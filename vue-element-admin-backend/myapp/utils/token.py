# 作者：我只是代码的搬运工
# coding:utf-8
from collections import namedtuple
from flask import request, current_app, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from myapp.utils.network import Result
from myapp.utils.scope import is_in_scope

auth = HTTPTokenAuth(scheme='JWT')
User = namedtuple('User', ['uid', 'scope'])  # 创建一个User对象


# token验证
@auth.verify_token
def verify_token(token):
    g.token_error = False
    g.token_timeout = False
    g.token_permission = False
    print("验证的token:===", token)
    user_info, status = verify_auth_token(token)
    if user_info and status:
        print("jwt验证成功!")
        g.user = user_info
        return True
    else:
        print("jwt验证失败!")
        return False


@auth.error_handler
def unauthorized():
    """
    auth认证失败的处理
    """
    if g.token_error:
        return Result.error(message="Token错误!")
    elif g.token_timeout:
        return Result.error(message="Token已过期!")
    elif g.token_permission:
        return Result.error(message="权限不足!")


# 验证token
def verify_auth_token(token):
    s = Serializer(current_app.config['JWT_SECRET'])
    if not token:
        g.token_error = True
        print("没有token")
        return Result.error(message="未传入token!"), False
    try:
        data = s.loads(token)  # 进行token验证

    except SignatureExpired:  # 过期了
        g.token_timeout = True
        print("过期了")
        return Result.error(message="token已过期!"), False
    except BadSignature:
        g.token_error = True
        print("token验证失败")
        return Result.error(message="token错误!"), False

    uid = data['uid']
    scope = data['scope']
    # 进行权限的功能的验证
    endpoint = request.endpoint.split('.')[1]
    allow = is_in_scope(scope, endpoint)  # 身份验证,判断是否视图函数是否合适
    if not allow:
        print("权限不够!")
        g.token_permission = True
        return Result.error(code=404, message="无此权限!"), False
    return User(uid, scope), True  # 返回一个对象

# # jwt认证
# def generate_access_token(username: str = "", algorithm: str = 'HS256', exp: float = 24, key: str = "sdfsdgfdsg"):
#     """
#     生成access_token
#     :param username: 用户名(自定义部分)
#     :param algorithm: 加密算法
#     :param exp: 过期时间
#     :return:token
#     """
#
#     now = datetime.now()
#     exp_datetime = now + timedelta(hours=exp)
#     access_payload = {
#         'exp': exp_datetime,
#         'flag': 0,  # 标识是否为一次性token，0是，1不是
#         'iat': now,  # 开始时间
#         'iss': 'leon',  # 签名
#         'username': username  # 用户名(自定义部分)
#         # 'publickey': RSAUtil.getPublicKey(username)  # 用户的公钥
#     }
#     access_token = jwt.encode(access_payload, key, algorithm=algorithm)
#     return access_token
#
#
# def decode_auth_token(token: str, key: str = "sdfsdgfdsg"):
#     """
#     解密token
#     :param token:token字符串
#     :return:
#     """
#     try:
#         payload = jwt.decode(token, key=key, algorithms='HS256')
#     except (jwt.ExpiredSignatureError, jwt.InvalidTokenError, jwt.InvalidSignatureError):
#         print("jwt解密失败!")
#         return Result.error(message="invalid_authorization_code")
#     else:
#         return payload
#
#
# def identify(auth_header: str, key: str):
#     """
#     用户鉴权
#     """
#     if auth_header:
#         # 解密head
#         payload = decode_auth_token(auth_header, key)
#         print("payload:===", payload)
#         if not payload:
#             return Result.error(message="invalid_authorization_code"), False
#         if "username" in payload and "flag" in payload:
#             if payload["flag"] == 0:
#                 return Result.success(data=payload["username"]), True
#             else:
#                 return Result.error(message="invalid_authorization_code"), False
#     return Result.error(message="invalid_authorization_code"), False
