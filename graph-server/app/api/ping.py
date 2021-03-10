from flask import jsonify
from app.api import bp


@bp.route('/ping', methods=['GET'])
def ping():
    """测试 API 是否通"""
    return jsonify('Test API pass！')