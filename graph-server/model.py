from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.matching import NodeMatcher, RelationshipMatcher
from queue import Queue
import json, re


def connectNeo4j():
    return Graph("http://localhost:7474", auth=("neo4j", "130340"))


def json2neo(data, graph):
    # with open('./templates/data.json', 'r') as f:
    #     data = json.load(f)

    graph.delete_all()

    nodeLabel = [
        'task',
        'method',
        'step',
        'attribute',
        'concept',
    ]
    nodes = []
    for node_json in data["nodes"]:
        try:
            node = Node(nodeLabel[node_json['groupId']], index=node_json['index'], label=node_json['label'],
                        groupId=node_json['groupId'])
        except KeyError:
            node = Node(nodeLabel[node_json['groupId']], index=node_json['index'], groupId=node_json['groupId'])
        nodes.append(node)
    kg = Subgraph(nodes)

    for link_json in data["links"]:
        link = Relationship(nodes[link_json['source']], 'links', nodes[link_json['target']])
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
        nodes_list.append({'index': node['index'], 'label': node['label'], 'groupId': node['groupId']})
    for link in list(links):
        links_list.append({'source': link.start_node['index'], 'target': link.end_node['index']})
    return {'nodes': nodes_list, 'links': links_list}


adjMatrix = {}
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
        for node in mainGraphData['nodes']:
            adjMatrix[node['index']] = downNodesFlag.copy()
        for link in mainGraphData['links']:
            adjMatrix[link['source']][link['target']] = 1

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


def md2json(mdName, jsonName):
    graphData = []
    text2deep = {
        '#': 0,
        '##': 1,
        '###': 2,
        '-': 3,
        '\t-': 4,
        '\t\t-': 5,
        '\t\t\t-': 6,
        '\t\t\t\t-': 7,
        '\t\t\t\t\t-': 8
    }
    text2groupId = {
        '任务': 0,
        '方法': 1,
        '步骤': 2,
        '属性': 3,
        '概念': 4
    }

    with open('./templates/' + mdName, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    index = 0
    for line in lines:
        if len(line) > 2:
            # print('------------------------------------------------------------------------')
            # print(line)
            line = line.replace('\n', '')
            line = re.split('[ ：\n]', line)
            line[0] = text2deep[line[0]]
            line.append(index)
            # print(line)
            if len(line) != 4:
                print(line)
            graphData.append(line)
            index += 1

    dfs = [graphData[0]]
    curDeep = graphData[0][0]
    nodes = [{'index': graphData[0][-1], 'label': graphData[0][2], 'groupId': text2groupId[graphData[0][1]]}]
    links = []
    for data in graphData[1:]:
        nodes.append({'index': data[-1], 'label': data[2], 'groupId': text2groupId[data[1]]})
        if data[0] <= curDeep:
            while dfs.pop()[0] > data[0]:
                continue
        curDeep = data[0]
        links.append({'source': dfs[-1][-1], 'target': data[-1]})
        dfs.append(data)

    with open('./templates/' + jsonName, 'w') as f:
        json.dump({'nodes': nodes, 'links': links}, f)


# graph = connectNeo4j()
# data = loadDataFromNeo4j(graph)
md2json('graph.md', 'data.json')