# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, request, g
from myapp.utils.network import Result
from myapp.utils.token import get_token, auth, verify_auth_token
from myapp.models.user import User

login_bp = Blueprint("login_bp", __name__)


@login_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()  # 输入的就是工号
    current_user, status = User.verify(data['username'], data['password'])  # 会获得user.id,与身份信息scope
    if status:
        # 获取token
        token = get_token(current_user['uid'], current_user['scope'])
        return Result.success(data=token)
    return current_user


# 获取用户信息,需认证token
@login_bp.route('/user/info', methods=['GET'])
@auth.login_required  # 验证X-Token
def get_info():
    token = request.args.get('token')  # 获取token
    uid = verify_auth_token(token)  # 验证token
    if uid:
        g.uid = uid
    info = User.query.filter_by(id=g.user.uid).first()  # 身份
    user_info = {
        "roles": [info.auth],
        "introduction": "introduction",
        "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
        "name": info.name
    }
    return Result.success(data=user_info)


# 退出路由
@login_bp.route('/user/logout', methods=['POST'])
def logout():
    return Result.success()
