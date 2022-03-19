# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :information_setting.py
# 时间    :2022/3/18 08:09
from rest_framework import mixins
from rest_framework.generics import GenericAPIView

from drf_vue_element_admin.myapps.information.serializers.information_setting import ChangeInformationSerializer, \
    ChangeAvatarSerializer, ChangePasswordSerializer


class ChangePasswordAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    put:
    个人中心--修改密码

    个人中心修改密码, status: 200(成功), return: None
    """
    serializer_class = ChangePasswordSerializer

    def put(self, request, *args, **kwargs):
        """
        使用put更新对象
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.update(request, *args, **kwargs)

    def get_object(self):
        """
        获取需要更新的对象
        :return:
        """
        return self.request.user


class ChangeInformationAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    put:
    个人中心--修改个人信息

    个人中心修改个人信息, status: 200(成功), return: 修改后的个人信息
    """
    serializer_class = ChangeInformationSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user


class ChangeAvatarAPIView(mixins.UpdateModelMixin, GenericAPIView):
    """
    put:
    个人中心--修改个人头像

    个人中心修改个人头像, status: 200(成功), return: 修改后的个人信息
    """
    serializer_class = ChangeAvatarSerializer

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def get_object(self):
        return self.request.user
