# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :permissions.py
# 时间    :2022/3/14 14:45
import json
import re

from django.conf import settings
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import BasePermission

from drf_vue_element_admin.common.permissions import redis_storage_permissions


class UserLock(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = '用户已被锁定,请联系管理员'
    default_code = 'not_authenticated'


class RbacPermission(BasePermission):
    """
    自定义权限认证
    """

    @staticmethod
    def pro_uri(uri):
        """
        设置静态方法将api的URL进行匹配出来
        :param uri:
        :return:
        """
        base_api = settings.BASE_API
        uri = '/' + base_api + '/' + uri + '/'
        return re.sub('/+', '/', uri)

    def has_permission(self, request, view):
        # 验证用户是否被锁定
        if not request.user.is_active:
            raise UserLock()
        request_url = request.path
        # 如果请求url在白名单，放行
        for safe_url in settings.WHITE_LIST:
            if re.match(settings.REGEX_URL.format(url=safe_url), request_url):
                return True
        # admin权限放行
        conn = get_redis_connection('user_info')
        if not conn.exists('user_permissions_manage'):
            redis_storage_permissions(conn)
        if conn.exists('user_info_%s' % request.user.id):
            user_permissions = json.loads(conn.hget('user_info_%s' % request.user.id, 'roles').decode())
            if 'admin' in user_permissions:
                return True
        else:
            user_permissions = []
            if 'admin' in request.user.roles.values_list('name', flat=True):
                return True
        # RBAC权限验证
