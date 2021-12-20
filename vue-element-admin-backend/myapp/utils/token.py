# 作者：我只是代码的搬运工
# coding:utf-8
from base64 import standard_b64decode
from collections import namedtuple
from datetime import datetime, timedelta
from flask import request, current_app, g
from flask_httpauth import HTTPBasicAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import jwt
from myapp.utils.network import Result
from myapp.utils.rsa_message import RSAUtil
from myapp.utils.scope import is_in_scope, user

auth = HTTPBasicAuth()
User = namedtuple('User', ['uid', 'scope'])  # 创建一个User对象


# token验证
@auth.verify_password
def verify_password(token, password):
    token = request.headers.get('X-Token')
    user_info, status = verify_auth_token(token)
    if user_info and status:
        print("验证成功!")
        g.user = user_info
        return True
    else:
        print("验证失败!")
        return False


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
        return Result.error(message="token错误!"), False
    except SignatureExpired:  # 过期了
        return Result.error(message="token已过期!"), False
    uid = data['uid']
    scope = data['scope']
    # 进行权限的功能的验证
    endpoint = request.endpoint.split('.')[1]
    allow = is_in_scope(scope, endpoint)  # 身份验证,判断是否视图函数是否合适
    if not allow:
        print("not allow")
        return Result.error(code=404, message="无此权限!"), False
    return User(uid, scope), True  # 返回一个对象


# jwt认证
def generate_access_token(username: str = "", algorithm: str = 'HS256', exp: float = 24, key: str = "sdfsdgfdsg"):
    """
    生成access_token
    :param username: 用户名(自定义部分)
    :param algorithm: 加密算法
    :param exp: 过期时间
    :return:token
    """

    now = datetime.now()
    exp_datetime = now + timedelta(hours=exp)
    access_payload = {
        'exp': exp_datetime,
        'flag': 0,  # 标识是否为一次性token，0是，1不是
        'iat': now,   # 开始时间
        'iss': 'leon',   # 签名
        'username': username  # 用户名(自定义部分)
        # 'publickey': RSAUtil.getPublicKey(username)  # 用户的公钥
    }
    access_token = jwt.encode(access_payload, key, algorithm=algorithm)
    return access_token


def decode_auth_token(token: str, key: str):
    """
    解密token
    :param token:token字符串
    :return:
    """
    try:
        payload = jwt.decode(token, key=key, algorithms='HS256')
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
        return Result.error(message="invalid_authorization_code")
    else:
        return Result.success(data=payload)


def identify(auth_header: str):
    """
    用户鉴权
    """
    if auth_header:
        # 解密head
        payload = decode_auth_token(auth_header)
        if not payload:
            return Result.error(message="invalid_authorization_code")
        if "username" in payload and "flag" in payload:
            if payload["flag"] == 0:
                return Result.success(data=payload["username"])
            else:
                return Result.error(message="invalid_authorization_code")
    return Result.error(message="invalid_authorization_code")
