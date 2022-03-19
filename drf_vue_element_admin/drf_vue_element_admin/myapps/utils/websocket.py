# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :websocket.py
# 时间    :2022/3/18 17:00
from urllib.parse import parse_qs

from django.db import close_old_connections
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class WebSocketTokenAuthentication(JSONWebTokenAuthentication):
    """
    重写token获取方式
    """

    def get_jwt_value(self, scope):
        """
        DRF-JWT获取token方法
        """
        token = parse_qs(scope['query_string'].decode('utf-8'))['token'][0]
        return token


class TokenAuthMiddleware:
    """
    自定义WebSocket验证方式
    """

    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        # 关闭旧的数据库连接以防止使用超时的连接
        close_old_connections()

        # 验证用户, 并获取user对象
        auth = WebSocketTokenAuthentication()
        user, token = auth.authenticate(scope)

        return self.inner(dict(scope, user=user))
