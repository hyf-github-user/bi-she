# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :oauth.py
# 时间    :2022/3/14 14:18
import json
from django.contrib.auth import get_user_model
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView
from rest_framework_jwt.views import ObtainJSONWebToken
from rest_framework import mixins, viewsets, views

from drf_vue_element_admin.myapps.oauth.serializers import UserRegSerializer

User = get_user_model()


class UserLoginView(ObtainJSONWebToken):
    """
    post:
    用户登录

    用户登录, status: 200(成功), return: Token信息
    """
    # 开放平台的API接口调用需要限制其频率，以节约服务器资源和避免恶意的频繁调用
    # 用于限制未认证用户的请求频率，主要根据用户的 IP地址来确定用户身份。
    throttle_classes = [AnonRateThrottle]

    def post(self, request, *args, **kwargs):
        # 重写父类方法, 定义响应字段内容
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            conn = get_redis_connection('user_info')
            conn.incr('visits')
            return response
        else:
            raise ValidationError(response.data)


class UserInfoView(APIView):
    """
    get:
    当前用户信息

    当前用户信息, status: 200(成功), return: 用户信息和权限
    """

    def get(self, request):
        user_info = request.user.get_user_info()
        # 将用户信息缓存到redis
        conn = get_redis_connection('user_info')
        # 防止第一次注册时没有设置角色,根据django自带的roles信息来设置,避免出现了俩个相同的roles
        if request.user.is_superuser and 'admin' not in user_info['roles']:
            user_info['roles'].append('admin')
        # 默认角色就是editor
        if not user_info['roles']:
            user_info['roles'].append('editor')
        # 将user_info转成Redis能存储的形式
        user_info['roles'] = json.dumps(user_info['roles'])
        user_info['avatar'] = request._current_scheme_host + user_info.get('avatar')
        conn.hmset('user_info_%s' % request.user.id, user_info)
        conn.expire('user_info_%s' % request.user.id, 60 * 60 * 24)  # 设置过期时间为1天
        user_info['roles'] = json.loads(user_info['roles'])
        return Response(user_info, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    """
    post:
    退出登录

    退出登录, status: 200(成功), return: None
    """

    def post(self, request):
        content = {}
        # 后续将增加redis token黑名单功能
        return Response(data=content)


class UserRegViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    注册视图
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = ()
    permission_classes = ()
