from app.api import bp
from flask import request


@bp.route('/push_data', methods=['POST', 'OPTIONS'])
def push_data():
    if request.method == 'POST':
        print(str(request.data, "utf-8"))

    return 'success'
