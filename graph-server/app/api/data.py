from app.api import bp
from flask import request, jsonify, url_for
import json, copy
from app import databaseMode
from model import *

if databaseMode:
    from app import graph

data = {}


@bp.route('/get_data', methods=['GET'])
def get_data():
    global data
    if databaseMode:
        data = loadDataFromNeo4j(graph)
    else:
        # print(request.json)
        with open('./templates/data.json', 'r') as f:
            data = json.load(f)
    return jsonify(data)


@bp.route('/post_data', methods=['POST', 'OPTIONS'])
def post_data():
    global data
    if request.method == 'POST':
        data = request.json

        nodes = []
        links = []
        for node in data["nodes"]:
            try:
                nodes.append({'index': node['index'], 'label': node['label'], 'groupId': node['groupId']})
            except KeyError:
                nodes.append({'index': node['index'], 'groupId': node['groupId']})
        for link in data["links"]:
            links.append({'source': link['source']['index'], 'target': link['target']['index']})
        data = {'nodes': nodes, 'links': links}

        if databaseMode:
            json2neo(data, graph)
        else:
            with open('./templates/data.json', 'w') as f:
                json.dump({'nodes': nodes, 'links': links}, f)

    return 'success'


indexNew2Old = {}
mainGraphData = {}


@bp.route('/get_subGraphData', methods=['GET'])
def get_subGraphData():
    global indexNew2Old
    global mainGraphData
    # print(indexNew2Old)
    # print(request.args['baseNodeIndex'])
    # try:
    #     print(indexNew2Old[int(request.args['baseNodeIndex'])])
    # except:
    #     pass

    if mainGraphData != data:
        mainGraphData = copy.deepcopy(data)
        updateAdjMatrix = False
    else:
        updateAdjMatrix = True
    try:
        subGraphData = adjSubgraph(mainGraphData, indexNew2Old[int(request.args['baseNodeIndex'])],
                                   int(request.args['numLayer']), updateAdjMatrix=updateAdjMatrix)
    except KeyError:
        subGraphData = adjSubgraph(mainGraphData, int(request.args['baseNodeIndex']), int(request.args['numLayer']),
                                   updateAdjMatrix=updateAdjMatrix)
    subGraphData, indexNew2Old = refreshIndex(subGraphData)
    return jsonify(subGraphData)


@bp.route('/get_mainGraphData', methods=['GET'])
def get_mainGraphData():
    return jsonify(data)
