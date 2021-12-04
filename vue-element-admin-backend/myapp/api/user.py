# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, request

from exts import db
from myapp.models.user import User
from myapp.utils import users_to_json
from myapp.utils.network import Result
import json

api_user = Blueprint("api_user", __name__)


# 获取用户列表
@api_user.route('/user/UserList', methods=['GET'])
def UserList():
    page = request.args.get('page', 1, type=int)
    size = request.args.get('size', 2, type=int)
    pagination = User.query.order_by(User.register_time.asc()).paginate(page, size, error_out=False)
    users = pagination.items
    users = users_to_json(users)
    total = User.query.all()
    total = len(total)
    if users:
        return Result.success(data=users, total=total)
    return Result.success()


# 根据id获取用户
@api_user.route('/user/getById', methods=['GET'])
def getById():
    id = request.args.get('id', type=int)
    user = User.query.get(id)
    if user:
        user = user.to_json()
        return Result.success(data=user)
    return Result.success()


# 更新用户信息
@api_user.route('/user/updateUser', methods=['PUT'])
def updateUser():
    data = request.get_data()
    data = json.loads(data)
    id = data.get('id')
    username = data.get('username')
    name = data.get('name')
    auth = data.get('auth')
    email = data.get('email')
    active = data.get('active')
    confirmed = data.get('confirmed')
    locked = data.get('locked')
    role_id = data.get('role_id')
    user = User.query.get(id)
    user.username = username
    user.name = name
    user.auth = auth
    user.email = email
    user.active = active
    user.confirmed = confirmed
    user.locked = locked
    user.role_id = role_id
    db.session.commit()
    return Result.success()


# 删除用户
@api_user.route('/user/deleteUser', methods=['DELETE'])
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
