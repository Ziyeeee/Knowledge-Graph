from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.matching import NodeMatcher, RelationshipMatcher
from queue import Queue
import json


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


def adjSubgraph(data, baseNodeIndex, numLayer):
    # initial
    downNodesFlag = {}
    upNodesFlag = {}
    nodesDict = {}
    adjMatrix = {}
    subAdjMatrix = {}
    bfsQueue = Queue()
    subGraphData = {'nodes': [], 'links': []}

    for node in data['nodes']:
        downNodesFlag[node['index']] = 0
        upNodesFlag[node['index']] = 0
        nodesDict[node['index']] = node
    for node in data['nodes']:
        adjMatrix[node['index']] = downNodesFlag.copy()
        subAdjMatrix[node['index']] = downNodesFlag.copy()
    for link in data['links']:
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
    nodeIndexDict = {}
    for node, index in zip(nodes, range(0, len(nodes))):
        nodeIndexDict[node['index']] = index
        node['index'] = index
    for link in data['links']:
        link['source'] = nodeIndexDict[link['source']]
        link['target'] = nodeIndexDict[link['target']]
    return data

# graph = connectNeo4j()
# data = loadDataFromNeo4j(graph)
# with open('./templates/data.json', 'r') as f:
#     data = json.load(f)
# data = adjSubgraph(data, 3, 2)
# print(data)
# data = refreshIndex(data)
# print(data)
