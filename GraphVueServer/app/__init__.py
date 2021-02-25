from flask import Flask
from config import Config
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# 数据库相关
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 跨域
    CORS(app)

    # 初始化数据库
    db.init_app(app)
    migrate.init_app(app, db)

    # 注册蓝图 blueprint
    from app.api import bp as api_bp
    app.register_blueprint(api_bp, url_prefix="/api")

    return app


from app import models

