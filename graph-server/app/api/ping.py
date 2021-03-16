from flask import make_response
from app.api import bp


@bp.route('/ping', methods=['GET'])
def ping():
    response = make_response('Ping success!')
    response.mimetype = 'text/plain'
    return response
