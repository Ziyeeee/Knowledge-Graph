from app.api import bp
from flask import request, jsonify
import json
from app import graph, databaseMode
from model import *


@bp.route('/get_data', methods=['GET'])
def get_data():
    if databaseMode:
        data = loadDataFromNeo4j(graph)
    else:
        # print(request.json)
        with open('./templates/data.json', 'r') as f:
            data = json.load(f)

    return jsonify(data)


@bp.route('/post_data', methods=['POST', 'OPTIONS'])
def post_data():
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
