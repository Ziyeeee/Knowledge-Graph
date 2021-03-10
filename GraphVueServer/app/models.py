import base64
import os
from _md5 import md5
from datetime import datetime, timedelta

import jwt
from flask import url_for, current_app

from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class PaginationAPIMixin:
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        # 分页查询，error_out 表示页数不是 int 或 超过总页数时，会报错，并返回 404，默认为 True
        resources = query.paginate(page, per_page, error_out=False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,  # 总页数
                'total_items': resources.total  # 总条数
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),  # "/api/users?page=1&per_page=10"
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next
                else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev
                else None
            }
        }
        return data


class User(PaginationAPIMixin, db.Model):
    """用户对象"""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)  # index 创建索引
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))  # 不保存原始密码
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # 使用 jwt
    def get_jwt(self, expire_in=3600):
        now = datetime.utcnow()
        payload = {
            'user_id': self.id,
            'name': self.name if self.name else self.username,
            'exp': now + timedelta(seconds=expire_in),
            'iat': now
        }

        return jwt.encode(
            payload,
            current_app.config['SECRET_KEY'],
            algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_jwt(token):
        try:
            payload = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError, jwt.exceptions.InvalidSignatureError) as e:
            # Token过期，或被人修改，那么签名验证也会失败
            return None
        return User.query.get(payload.get('user_id'))

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    # # token 验证 API（需要登录才能请求）
    # token = db.Column(db.String(32), index=True, unique=True)
    # token_expiration = db.Column(db.DateTime)   # token 过期时间

    # def get_token(self, expires_in=3600):
    #     now = datetime.utcnow()
    #     # 大于 一分钟
    #     if self.token and self.token_expiration > now + timedelta(seconds=60):
    #         return self.token
    #
    #     self.token = base64.b64encode(os.urandom(24)).decode('utf-8')   # 生成 token
    #     self.token_expiration = now + timedelta(seconds=expires_in)
    #     db.session.add(self)
    #     return self.token
    #
    # def revoke_token(self):
    #     """撤销 token，当前 utc 时间减去 1 秒"""
    #     self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
    #
    # @staticmethod
    # def check_token(token):
    #     """检查 token"""
    #     user = User.query.filter_by(token=token).first()
    #     # 若没有 token 或者 token 已过期，返回 None，不准请求
    #     if user is None or user.token_expiration < datetime.utcnow():
    #         return None
    #     return user

    def __str__(self):
        return '<User {}>'.format(self.username)

    def generate_password(self, password):
        """密码哈希"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """检查密码是否正确"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self, include_email=False):
        """
        封装 User 对象，传递给前端只能是 json 格式，不能是实例对象
        :param include_email: 只有当用户请求自己数据时，才包含 email
        :return:
        """
        data = {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'location': self.location,
            'about_me': self.about_me,
            'member_since': self.member_since.isoformat() + 'Z',
            'last_seen': self.last_seen.isoformat() + 'Z',
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'avatar': self.avatar(128)
            }
        }
        if include_email:
            data['email'] = self.email

        return data

    def from_dict(self, data, new_user=False):
        """
        将前端发送过来的 json 对象转换为 User 对象
        :param data:
        :param new_user:
        :return:
        """
        for field in ['username', 'email', 'name', 'location', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
            if new_user and 'password' in data:
                self.generate_password(data['password'])

    def avatar(self, size):
        """
        使用 Gravatar 服务，根据 email 生成头像
        使用 https://en.gravatar.com/
        :param size:
        :return:
        """
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)