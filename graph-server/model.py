from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.ogm import GraphObject, Property
import json


class KGNode(GraphObject):
    __primarykey__ = 'index'

    label = Property()
    groupId = Property()


# class Link(GraphObject):
#     __primarykey__ = 'link_id'
#
#     source = Property()
#     target = Property()


with open('./templates/data.json', 'r') as f:
    data = json.load(f)
graph = Graph("http://localhost:7474", auth=("neo4j", "130340"))

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
    node = Node(nodeLabel[node_json['groupId']], index=node_json['index'], label=node_json['label'], groupId=node_json['groupId'])
    nodes.append(node)
kg = Subgraph(nodes)

for link_json in data["links"]:
    link = Relationship(nodes[link_json['source']], 'links', nodes[link_json['target']])
    kg = kg | link

# graph.create(sg_nodes)
graph.create(kg)
