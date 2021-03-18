from flask import Flask
from config import Config
from flask_cors import CORS
from model import connectNeo4j


databaseMode = False
if databaseMode:
    graph = connectNeo4j()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 跨域
    CORS(app, supports_credentials=True, methods=['GET', 'POST'])

    # 注册蓝图 blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app