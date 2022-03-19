# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :routing.py
# 时间    :2022/3/18 16:57
# WebSocket路由
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from drf_vue_element_admin.myapps.utils.websocket import TokenAuthMiddleware
from drf_vue_element_admin.myapps.monitor.consumers import service


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'drf_vue_element_admin.settings')
django.setup()
application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter([
            re_path(r'^monitor/service', service.ResourcesConsumer),
        ])
    )
})
