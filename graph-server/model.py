from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.matching import NodeMatcher, RelationshipMatcher
from queue import Queue
from jieba import load_userdict, cut_for_search
import json
from gensim.models import KeyedVectors


adjMatrix = {}
nodeLabel = [
    '任务',
    '方法',
    '步骤',
    '属性',
    '概念',
]


def connectNeo4j():
    return Graph("http://localhost:7474", auth=("neo4j", "130340"))


def json2neo(data, graph):
    # with open('./templates/data.json', 'r') as f:
    #     data = json.load(f)

    graph.delete_all()

    nodes = []
    for node_json in data["nodes"]:
        try:
            node = Node(nodeLabel[node_json['groupId']], index=node_json['index'], label=node_json['label'],
                        reference=node_json['reference'], groupId=node_json['groupId'])
        except KeyError:
            node = Node(nodeLabel[node_json['groupId']], index=node_json['index'], groupId=node_json['groupId'],
                        reference=node_json['reference'])
        nodes.append(node)
    kg = Subgraph(nodes)

    for link_json in data["links"]:
        linkLabel = str(nodes[link_json['target']].labels)[1:]
        link = Relationship(nodes[link_json['source']], linkLabel, nodes[link_json['target']])
        kg = kg | link

    # graph.create(sg_nodes)
    graph.create(kg)


def loadDataFromNeo4j(graph):
    nodeMatcher = NodeMatcher(graph)
    linkMatcher = RelationshipMatcher(graph)
    nodes = nodeMatcher.match().order_by('_.index')
    links = linkMatcher.match()

    nodes_list = []
    links_list = []
    for node in list(nodes):
        radius = 30
        # radius = 30 + calculateOutDegree(node['index']) * 5
        # if radius > 60:
        #     radius = 90
        nodes_list.append(
            {'index': node['index'], 'label': node['label'], 'reference': node['reference'], 'groupId': node['groupId'],
             'radius': radius})
    for link in list(links):
        links_list.append({'source': link.start_node['index'], 'target': link.end_node['index']})
    return {'nodes': nodes_list, 'links': links_list}


def loadDataFromJson(fileName):
    with open(fileName, 'r') as f:
        return json.load(f)


def calculateOutDegree(index, data):
    global adjMatrix
    inniAdjMatrix(data)
    cnt = 0
    for value in adjMatrix[index].values():
        if value:
            cnt += 1
    return cnt


def inniAdjMatrix(data):
    global adjMatrix
    node_dict = {}
    for node in data['nodes']:
        node_dict[node['index']] = 0
    for node in data['nodes']:
        adjMatrix[node['index']] = node_dict.copy()
    for link in data['links']:
        adjMatrix[link['source']][link['target']] = 1
    # print(adjMatrix)


def adjSubgraph(mainGraphData, baseNodeIndex, numLayer, updateAdjMatrix=True):
    # initial
    downNodesFlag = {}
    upNodesFlag = {}
    nodesDict = {}
    global adjMatrix
    subAdjMatrix = {}
    bfsQueue = Queue()
    subGraphData = {'nodes': [], 'links': []}

    for node in mainGraphData['nodes']:
        downNodesFlag[node['index']] = 0
        upNodesFlag[node['index']] = 0
        nodesDict[node['index']] = node
    for node in mainGraphData['nodes']:
        subAdjMatrix[node['index']] = downNodesFlag.copy()

    if updateAdjMatrix:
        inniAdjMatrix(mainGraphData)
        # print(adjMatrix)

    # down
    bfsQueue.put(baseNodeIndex)
    for i in range(0, numLayer):
        len = bfsQueue.qsize()
        for j in range(0, len):
            nodeIndex = bfsQueue.get()
            if downNodesFlag[nodeIndex] == 0:
                downNodesFlag[nodeIndex] = 1
                for (targetIndex, flag) in adjMatrix[nodeIndex].items():
                    if flag:
                        bfsQueue.put(targetIndex)
                        subAdjMatrix[nodeIndex][targetIndex] = flag
    while not bfsQueue.empty():
        nodeIndex = bfsQueue.get()
        if downNodesFlag[nodeIndex] == 0:
            downNodesFlag[nodeIndex] = 1

    # up
    bfsQueue.put(baseNodeIndex)
    for i in range(0, numLayer):
        len = bfsQueue.qsize()
        for j in range(0, len):
            nodeIndex = bfsQueue.get()
            if upNodesFlag[nodeIndex] == 0:
                upNodesFlag[nodeIndex] = 1
                for key in adjMatrix.keys():
                    flag = adjMatrix[key][nodeIndex]
                    if flag:
                        bfsQueue.put(key)
                        subAdjMatrix[key][nodeIndex] = flag
    while not bfsQueue.empty():
        nodeIndex = bfsQueue.get()
        if upNodesFlag[nodeIndex] == 0:
            upNodesFlag[nodeIndex] = 1

    # print(upNodesFlag, downNodesFlag)
    nodesFlag = {}
    for upNode, downNode in zip(upNodesFlag.items(), downNodesFlag.items()):
        if upNode[1] or downNode[1]:
            subGraphData['nodes'].append(nodesDict[upNode[0]])
    for sourceIndex in subAdjMatrix.keys():
        for (targetIndex, flag) in subAdjMatrix[sourceIndex].items():
            if flag:
                subGraphData['links'].append({'source': sourceIndex, 'target': targetIndex})
    return subGraphData


def refreshIndex(data):
    nodes = data['nodes']
    indexOld2New = {}
    indexNew2Old = {}
    for node, index in zip(nodes, range(0, len(nodes))):
        indexOld2New[node['index']] = index
        node['index'] = index

    for link in data['links']:
        link['source'] = indexOld2New[link['source']]
        link['target'] = indexOld2New[link['target']]
    for (key, value) in indexOld2New.items():
        indexNew2Old[value] = key
    return data, indexNew2Old


def searchSubGraph(graph, mainGraphData, search, numLayer, isRecommend, updateAdjMatrix=True):
    # search = '关联规则挖掘'
    subGraphData = False
    nodeMatcher = NodeMatcher(graph)
    print(search)
    model = KeyedVectors.load_word2vec_format('./DeepWalkModel/deepwalkModel', binary=False, encoding="utf8")


    if isRecommend == 'true':
        nodesIndex = []
        nodes_list = []
        nodeAndLink = search.split('的')

        cql = 'MATCH (fn) WHERE fn.label = \'' + nodeAndLink[0] + '\' RETURN fn'
        nodes = graph.run(cql).data()
        for node in nodes:
            nodesIndex.append(node['fn']['index'])
            nodes_list.append({'index': node['fn']['index'], 'label': node['fn']['label'],
                               'groupId': node['fn']['groupId']})

        cql = 'MATCH (fn)-[r:' + nodeAndLink[1] + ']->(tn) WHERE fn.label = \'' + nodeAndLink[0] + '\' RETURN tn'
        nodes = graph.run(cql).data()
        for node in nodes:
            nodesIndex.append(node['tn']['index'])
            nodes_list.append({'index': node['tn']['index'], 'label': node['tn']['label'],
                               'groupId': node['tn']['groupId']})

        # 根据节点找出节点间关系
        links_list = findLinksByNodesIndex(nodesIndex)
        subGraphData = {'nodes': nodes_list, 'links': links_list}
    elif isRecommend == 'false':
        load_userdict('user_dict.txt')
        search_list = cut_for_search(search)

        nodes = nodeMatcher.match(label=search).order_by('_.index')
        for node in nodes:
            # print(node)
            tempSubGraphData = adjSubgraph(mainGraphData, node['index'], numLayer, updateAdjMatrix=updateAdjMatrix)
            if subGraphData:
                subGraphData = mergeGraph(subGraphData, tempSubGraphData)
            else:
                subGraphData = tempSubGraphData

        for key in search_list:
            print(key)
            nodes = nodeMatcher.match(label=key).order_by('_.index')
            for node in nodes:
                # print(node)
                tempSubGraphData = adjSubgraph(mainGraphData, node['index'], numLayer, updateAdjMatrix=updateAdjMatrix)
                if subGraphData:
                    subGraphData = mergeGraph(subGraphData, tempSubGraphData)
                else:
                    subGraphData = tempSubGraphData

    return subGraphData


def mergeGraph(graph0, graph1):
    nodes_dict = {}

    for node in graph0['nodes']:
        nodes_dict[node['index']] = node
    for node in graph1['nodes']:
        nodes_dict[node['index']] = node
    # print(nodes_dict.keys())

    links_set = set()
    for link in graph0['links']:
        links_set.add(link.values())
    for link in graph1['links']:
        links_set.add(link.values())
    # print(links_set)

    nodes_list = []
    links_list = []
    for node in nodes_dict.values():
        nodes_list.append(node)
    for link in links_set:
        link = list(link)
        links_list.append({'source': link[0], 'target': link[1]})
    # print({'nodes': nodes_list, 'links': links_list})
    return {'nodes': nodes_list, 'links': links_list}


def findLinksByNodesIndex(nodesIndex):
    global adjMatrix
    links = []

    for index in nodesIndex:
        for key in adjMatrix[index].keys():
            if adjMatrix[index][key] == 1 and key in nodesIndex:
                links.append({'source': index, 'target': key})
    return links


def autoComplete(graph, search):
    load_userdict('user_dict.txt')
    search_list = list(cut_for_search(search))
    search_list.insert(0, search)
    print(search_list)
    similarNode = []
    for key in search_list:
        similarNode += findInterdependentNode(key)
    search_list = list(search_list) + similarNode + findInterdependentNode(search)
    search_list = list(set(search_list))
    print(search_list)

    autoCompleteList = []
    for key in search_list:
        cql = 'MATCH (fn)-[r]->(tn) WHERE fn.label = \'' + key + '\' RETURN tn.groupId'
        # try:
        nodes = graph.run(cql).data()
        groupIds = set(node['tn.groupId'] for node in nodes)
        for groupId in groupIds:
            autoCompleteList.append({'value': key + '的' + nodeLabel[groupId]})
        # except:
        #     print(cql)
    return autoCompleteList


def findInterdependentNode(word):
    global model
    res = []
    try:
        labels = model.most_similar(word, topn=50)
        for label in labels:
            if len(label[0]) < 7:
                res.append(label[0])
            if len(res) > 5:
                break
        return res
    except:
        return []

model = KeyedVectors.load_word2vec_format('./DeepWalkModel/deepwalkModel', binary=False, encoding="utf8")

# graph = connectNeo4j()
# data = loadDataFromNeo4j(graph)
# md2json('graph.md', 'data.json')

# with open('./templates/data.json', 'r') as f:
#     data = json.load(f)

# json2neo(data, graph)

# autoComplete(graph, '关联规则挖掘')

# userDict = []
#     inniAdjMatrix(data)
#     for node in data['nodes']:
#         if node['groupId'] == 4 or (node['groupId'] != 3 and len(node['label']) < 7):
#             cnt = 1
#             for key in adjMatrix.keys():
#                 if adjMatrix[key][node['index']]:
#                     cnt += 1
#             userDict.append(node['label'] + ' ' + str(cnt) + ' nz\n')
#     with open('user_dict.txt', 'w', encoding='utf-8') as f:
#         f.writelines(userDict)



