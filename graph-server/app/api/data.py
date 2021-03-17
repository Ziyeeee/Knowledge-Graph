from app.api import bp
from flask import request, jsonify
import json
from app import graph
from model import *


@bp.route('/get_data', methods=['GET'])
def get_data():
    # print(request.json)
    # with open('./templates/data.json', 'r') as f:
    #     data = json.load(f)
    data = loadDataFromNeo4j(graph)

    return jsonify(data)


@bp.route('/post_data', methods=['POST', 'OPTIONS'])
def post_data():
    if request.method == 'POST':
        data = request.json

        nodes = []
        links = []
        for node in data["nodes"]:
            # print(node)
            try:
                nodes.append({'index': node['index'], 'label': node['label'], 'groupId': node['groupId']})
            except KeyError:
                nodes.append({'index': node['index'], 'groupId': node['groupId']})
        for link in data["links"]:
            # print(link)
            links.append({'source': link['source']['index'], 'target': link['target']['index']})
        data = {'nodes': nodes, 'links': links}
        # with open('./templates/data.json', 'w') as f:
        #     json.dump({'nodes': nodes, 'links': links}, f)

        json2neo(data, graph)

    return 'success'
