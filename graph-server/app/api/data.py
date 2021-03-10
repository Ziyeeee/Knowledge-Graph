from app.api import bp
from flask import request, jsonify
import json


@bp.route('/get_data', methods=['GET'])
def get_data():
    print(request.json)
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
            # print(node)
            nodes.append({'index': node['index'], 'label': node['label'], 'groupId': node['groupId']})
        for link in data["links"]:
            # print(link)
            links.append({'source': link['source']['index'], 'target': link['target']['index']})
        print({'nodes': nodes, 'links': links})
        with open('./templates/data.json', 'w') as f:
            json.dump({'nodes': nodes, 'links': links}, f)
    return 'success'
