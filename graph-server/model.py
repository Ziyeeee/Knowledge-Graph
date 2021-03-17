from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.matching import NodeMatcher, RelationshipMatcher
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
            node = Node(nodeLabel[node_json['groupId']], index=node_json['index'], label=node_json['label'], groupId=node_json['groupId'])
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

