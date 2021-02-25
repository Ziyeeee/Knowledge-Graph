from flask import jsonify
from werkzeug.http import HTTP_STATUS_CODES

from app import db
from app.api import bp


def error_response(status_code, message=None):
    payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknow error')}
    if message:
        payload['message'] = message

    response = jsonify(payload)
    response.status_code = status_code
    return response


def bad_request(message):
    """
    异常请求，如：400
    :param message:
    :return:
    """
    return error_response(400, message)


@bp.app_errorhandler(404)
def not_found_error(error):
    return error_response(404)


@bp.app_errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return error_response(500)
