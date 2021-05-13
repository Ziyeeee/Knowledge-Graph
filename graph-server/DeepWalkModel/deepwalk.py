import json
from py2neo import Graph, Node, Relationship, Subgraph
from py2neo.matching import NodeMatcher, RelationshipMatcher
from gensim.models import KeyedVectors, Word2Vec
from jieba import cut, load_userdict, cut_for_search
import re
from zhon.hanzi import punctuation as cn_punctuation
from string import punctuation as en_punctuation
import random


def connectNeo4j():
    return Graph("http://localhost:7474", auth=("neo4j", "130340"))


def loadDataFromNeo4j(graph):
    nodeMatcher = NodeMatcher(graph)
    linkMatcher = RelationshipMatcher(graph)
    nodes = nodeMatcher.match().order_by('_.index')
    links = linkMatcher.match()

    nodes_list = []
    links_list = []
    for node in list(nodes):
        nodes_list.append(
            {'index': node['index'], 'label': node['label'], 'groupId': node['groupId']})
    for link in list(links):
        links_list.append({'source': link.start_node['index'], 'target': link.end_node['index']})
    return {'nodes': nodes_list, 'links': links_list}


def inniAdjMatrix(data):
    adjMatrix = {}
    node_dict = {}
    for node in data['nodes']:
        node_dict[node['index']] = 0
    for node in data['nodes']:
        adjMatrix[node['index']] = node_dict.copy()
    for link in data['links']:
        adjMatrix[link['source']][link['target']] = 1
    # print(adjMatrix)
    return adjMatrix


def getRandomWalk(nodes, adjMatrix, node, path_length):
    randomWalk = [node['label']]

    startNode = node
    for i in range(0, path_length):
        temp = []
        for key, value in adjMatrix[node['index']].items():
            if value == 1:
                temp.append(nodes[key])
        if len(temp) == 0:
            break

        randomNode = random.choice(temp)
        randomWalk.append(randomNode['label'])
        node = randomNode

    node = startNode
    for i in range(0, path_length):
        temp = []
        for key in adjMatrix.keys():
            if adjMatrix[key][node['index']] == 1:
                temp.append(nodes[key])
        if len(temp) == 0:
            break

        randomNode = random.choice(temp)
        randomWalk.insert(0, randomNode['label'])
        node = randomNode
    return randomWalk


def deepWalk(walkTimes, pathDeep):
    graph = connectNeo4j()
    data = loadDataFromNeo4j(graph)
    adjMatrix = inniAdjMatrix(data)
    randomWalks = []
    nodes = data['nodes']
    for i in range(0, len(nodes)):
        for j in range(0, walkTimes):
            randomWalks.append(getRandomWalk(nodes, adjMatrix, nodes[i], pathDeep))
    return randomWalks


randomWalks = deepWalk(15, 5)
print(len(randomWalks))

model = Word2Vec(vector_size=50, window=3, sg=1, hs=0, negative=10, alpha=0.02, min_alpha=0.0005, seed=14)

model.build_vocab(randomWalks, progress_per=2)

model.train(randomWalks, total_examples=model.corpus_count, epochs=20)
print(model.wv.most_similar('支持度', topn=100))
model.wv.save_word2vec_format('deepwalkModel')
model = KeyedVectors.load_word2vec_format('deepwalkModel', binary=False, encoding="utf8")
print(model.most_similar('支持度', topn=100))
