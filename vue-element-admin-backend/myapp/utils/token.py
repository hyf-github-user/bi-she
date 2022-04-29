# 作者：我只是代码的搬运工
# coding:utf-8
from collections import namedtuple
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
from exts import db
from settings import Operations

User = namedtuple('User', ['uid', 'scope'])  # 创建一个User对象


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
