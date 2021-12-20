# 作者：我只是代码的搬运工
# coding:utf-8
import json
from myapp.utils.network import Result
from myapp.utils import users_to_json
from myapp.models.user import User
from exts import db
from flask import Blueprint, request
from myapp.utils.token import auth

api_user = Blueprint("api_user", __name__)


# 获取用户列表
@api_user.route('/user/UserList', methods=['GET'])
@auth.login_required  # 验证X-Token
def UserList():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 2, type=int)
    pagination = User.query.order_by(
        User.register_time.asc()).paginate(page, size, error_out=False)
    users = pagination.items
    users = users_to_json(users)
    total = User.query.all()
    total = len(total)
    if users:
        return Result.success(data=users, total=total)
    return Result.success()


# 根据id获取用户
@api_user.route('/user/getById', methods=['GET'])
@auth.login_required  # 验证X-Token
def getById():
    id = request.args.get('id', type=int)
    user = User.query.get(id)
    if user:
        user = user.to_json()
        return Result.success(data=user)
    return Result.success()


# 更新用户信息
@api_user.route('/user/updateUser', methods=['PUT'])
@auth.login_required  # 验证X-Token
def updateUser():
    data = request.get_data()
    data = json.loads(data)
    id = data.get('id')
    username = data.get('username')
    name = data.get('name')
    email = data.get('email')
    active = data.get('active')
    confirmed = data.get('confirmed')
    role_id = data.get('role_id')
    locked = data.get('locked')
    user = User.query.get(id)
    user.update(username=username, name=name,
                email=email, active=active,
                locked=locked,
                confirmed=confirmed, role_id=role_id)
    db.session.commit()
    return Result.success()


# 删除用户
@api_user.route('/user/deleteUser', methods=['DELETE'])
@auth.login_required  # 验证X-Token
def deleteUser():
    id = request.args.get('id', type=int)
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        print("我要删除它")
        return Result.success()
    return Result.success()


# 添加用户
@api_user.route('/user/addUser', methods=['POST'])
@auth.login_required  # 验证X-Token
def addUser():
    data = request.get_data()
    data = json.loads(data)
    username = data.get('username')
    name = data.get('name')
    auth = data.get('auth')
    email = data.get('email')
    active = data.get('active')
    if active == '1':
        active = True
    else:
        active = False
    confirmed = data.get('confirmed')
    if confirmed == '1':
        confirmed = True
    else:
        confirmed = False
    locked = data.get('locked')
    if locked == '1':
        locked = True
    else:
        locked = False
    role_id = data.get('role_id')
    password = data.get('password')
    user = User(username=username,
                name=name,
                auth=auth,
                email=email,
                active=active,
                confirmed=confirmed,
                locked=locked,
                role_id=role_id)
    user.set_password(password)
    user.set_hash_password()
    db.session.add(user)
    db.session.commit()
    return Result.success()
