from flask import g, jsonify

from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth


# @bp.route('/tokens', methods=['POST'])
# @basic_auth.login_required
# def get_token():
#     token = g.current_user.get_token()
#     db.session.commit()
#     return jsonify({'token': token})

@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
    """
    每次用户登录成功后（获取到jwt），更新 last_seen 时间
    jwt 不能删除，只能等其自己过期
    :return:
    """
    token = g.current_user.get_jwt()
    # print('token===>', token)

    # 每次用户登录（即成功获取 JWT 后），更新 last_seen 时间
    g.current_user.ping()
    db.session.commit()
    return jsonify({'token': token})


# @bp.route('/tokens', methods=['DELETE'])
# @token_auth.login_required
# def revoke_token():
#     g.current_user.revoke_token()
#     db.session.commit()
#     return '', 204
