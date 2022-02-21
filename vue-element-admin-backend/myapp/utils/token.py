# 作者：我只是代码的搬运工
# coding:utf-8
from collections import namedtuple
from flask import request, current_app, g
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired

from exts import db
from myapp.utils.network import Result
from myapp.utils.scope import is_in_scope
from settings import Operations

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
    # # 进行权限的功能的验证
    # endpoint = request.endpoint.split('.')[1]
    # allow = is_in_scope(scope, endpoint)  # 身份验证,判断是否视图函数是否合适
    # if not allow:
    #     print("权限不够!")
    #     g.token_permission = True
    #     return Result.error(code=404, message="无此权限!"), False
    return User(uid, scope), True  # 返回一个对象


def generate_token(user, operation, expire_in=None, **kwargs):
    """
    在前台的登录设置token注册验证
    :param user:
    :param operation:
    :param expire_in:
    :param kwargs:
    :return:
    """
    token = Serializer(current_app.config['SECRET_KEY'], expire_in)  # 生成token并设置过期时间
    # token内包含的数据
    data = {'id': user.id, 'operation': operation}
    data.update(**kwargs)
    return token.dumps(data)


def validate_token(user, token, operation, new_password=None):
    """
    验证token,并进行相应的操作
    :param user:
    :param token:
    :param operation:
    :param new_password:
    :return:
    """
    s = Serializer(current_app.config['SECRET_KEY'])
    try:
        # 解析token的信息
        data = s.loads(token)
    except SignatureExpired:
        print("token过期了!")
        return False
    except BadSignature:
        print("token错误!")
        return False
    # 判断token的数据是不是正确的
    if operation != data.get('operation') or user.id != data.get('id'):
        return False
    # 检查operation
    if operation == Operations.CONFIRM:  # 确认
        user.confirmed = True
    elif operation == Operations.RESET_PASSWORD:  # 重设密码
        user.set_password(new_password)
    elif operation == Operations.CHANGE_EMAIL:  # 更新电子邮件
        new_email = data.get('new_email')  # 新的email
        if new_email is None:
            return False
        if User.query.filter_by(email=new_email).first() is not None:
            return False
        user.email = new_email
    else:
        return False
    # 更新数据库字段
    db.session.commit()
    return True
