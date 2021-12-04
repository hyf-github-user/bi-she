# 作者：我只是代码的搬运工
# coding:utf-8
from myapp.utils.error import APIException


# HTTP消息状态码
# 认证失败
class AuthFailed(APIException):
    code = 401
    error_code = 1005
    msg = 'authorization failed'


# 参数错误
class ParameterException(APIException):
    code = 400
    msg = 'invalid parameter'
    error_code = 1000


class Forbidden(APIException):
    code = 403
    error_code = 1004
    msg = 'forbidden, not in scope'
