from app import create_app, db
from app.models import User

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """配置flask shell 上下文"""
    return {'db': db, 'User': User}
