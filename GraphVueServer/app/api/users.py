import re

from flask import jsonify, request, url_for, g
from sqlalchemy import or_

from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import User


@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    """用户集合，分页"""
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)
    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')
    return jsonify(data)


@bp.route('/users', methods=['POST'])
def create_user():
    """创建一个新用户"""
    data = request.get_json()

    if not data:
        return bad_request("post 必须是 json 数据！")

    message = {}
    username = data.get('username', None)
    email = data.get('email', None)
    password = data.get('password', None)

    # 判断是否为空
    if 'username' not in data or not username:
        message['username'] = "请提供一个有效的用户名！"
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' not in data or not re.match(pattern, email):
        message['email'] = "请提供一个有效的邮箱地址！"
    if 'password' not in data or not password:
        message['password'] = "请提供一个有效的密码！"

    # 检查数据库中是否有该用户
    if User.query.filter(or_(User.username == username, User.email == email)).first():
        message['username'] = "用户名或邮箱已存在！"

    if message:
        return bad_request(message)

    # 创建新用户
    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201

    response.headers['Location'] = url_for('api.get_user', id=user.id)  # /api/users/1
    return response


@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    """返回一个用户"""
    user = User.query.get_or_404(id)
    if g.current_user == user:
        return jsonify(User.query.get_or_404(id).to_dict(include_email=True))
    return jsonify(User.query.get_or_404(id).to_dict())


@bp.route('/users/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_user(id):
    """修改一个用户"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    print(data)
    if not data:
        return bad_request("post 必须是 json 数据！")

    message = {}
    username = data.get('username', None)
    email = data.get('email', None)

    # 判断是否为空
    if 'username' in data and not username:
        message['username'] = "请提供一个有效的用户名！"
    pattern = '^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$'
    if 'email' in data and not re.match(pattern, email):
        message['email'] = "请提供一个有效的邮箱地址！"

    if 'username' in data and data['username'] != user.username and \
            User.query.filter_by(username=data['username']).first():
        message['username'] = '请使用一个不同的用户名！'
    if 'email' in data and data['email'] != user.email and \
            User.query.filter_by(email=data['email']).first():
        message['email'] = '请使用一个不同的邮箱！'

    if message:
        return bad_request(message)

    user.from_dict(data, new_user=False)
    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    """删除一个新用户"""
    pass
