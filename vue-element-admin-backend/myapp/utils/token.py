# 作者：我只是代码的搬运工
# coding:utf-8
from collections import namedtuple
from flask import request, current_app, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from myapp.utils.network import Result
from myapp.utils.scope import is_in_scope

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'scope'])  # 创建一个User对象


# token验证
@auth.verify_password
def verify_password(token, password):
    token = request.headers.get('X-Token')
    user_info = verify_auth_token(token)

    if not user_info:
        return False
    else:
        g.user = user_info
        return True


# 获取token
def get_token(uid, scope):
    expiration = current_app.config['TOKEN_EXPIRATION']  # token过期时间
    token = generate_auth_token(
        uid,
        scope,
        expiration
    )
    # 进行ASCII编码
    t = {
        'token': token.decode('ascii')
    }
    return t


# 生成token
def generate_auth_token(uid, scope=None, expiration=7200):
    s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)

    return s.dumps({
        'uid': uid,
        'scope': scope
    })


# 验证token
def verify_auth_token(token):
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        data = s.loads(token)  # 进行token验证
    except BadSignature:
        return Result.error(message="token错误!")
    except SignatureExpired:  # 过期了
        return Result.error(message="token已过期!")
    uid = data['uid']
    scope = data['scope']
    # 进行权限的功能的验证
    blueprint = request.blueprint
    split = blueprint.split('_')
    allow = is_in_scope(scope, request.endpoint, split[0])  # 身份验证,判断是否视图函数是否合适
    if not allow:
        return Result.error(message="无此权限!")
    return User(uid, scope)  # 返回一个对象
