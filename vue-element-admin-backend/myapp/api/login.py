# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, request, g
from myapp.utils.token import generate_access_token
from myapp.utils.network import Result
from myapp.utils.token import get_token, auth, verify_auth_token
from myapp.models.user import User

login_bp = Blueprint("login_bp", __name__)


@login_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json()  # 输入的就是工号
    current_user, status = User.verify(
        data['username'], data['password'])  # 会获得user.id,与身份信息scope
    if status:
        # 获取token
        token = get_token(current_user['uid'], current_user['scope'])
        jwt_token = generate_access_token(current_user['uid'])
        return Result.success(data=token, jwt=jwt_token)
    print("current_user:", current_user)
    return current_user


# 获取用户信息,需认证token
@login_bp.route('/user/info', methods=['GET'])
@auth.login_required  # 验证X-Token
def get_info():
    token = request.args.get('token')  # 获取token
    user, status = verify_auth_token(token)  # 验证token
    if status and user:
        g.user = user
        info = User.query.filter_by(id=g.user.uid).first()  # 身份
        user_info = {
            "roles": [info.username],
            "introduction": "introduction",
            "avatar": "https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name": info.name
        }
        # print("user_info:====", user_info)
        return Result.success(data=user_info)
    else:
        return user


# 退出路由
@login_bp.route('/user/logout', methods=['POST'])
def logout():
    return Result.success()
