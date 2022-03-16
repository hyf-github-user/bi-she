# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :service.py
# 时间    :2022/3/16 22:40
import platform
import socket

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class ServiceMonitorAPIView(APIView):
    """
    get:
    监控--服务监控

    获取服务器信息, status: 200(成功), return: 服务器信息
    """

    def get(self, request):
        service_info = dict()
        service_info['platform'] = platform.platform()
        service_info['ip'] = self.get_host_ip()
        return Response(service_info, status=status.HTTP_200_OK)

    @staticmethod
    def get_host_ip():
        """
        查询本机ip地址
        :return: ip
        """
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('8.8.8.8', 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
        return ip
