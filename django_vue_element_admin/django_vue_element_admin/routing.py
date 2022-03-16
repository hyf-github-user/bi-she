# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :routing.py
# 时间    :2022/3/14 07:20
# WebSocket路由
import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django_vue_element_admin.myapps.utils.websocket import TokenAuthMiddleware
from django_vue_element_admin.myapps.monitor.consumers import service


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'vue_element_admin_django.settings')
django.setup()
application = ProtocolTypeRouter({
    'websocket': TokenAuthMiddleware(
        URLRouter([
            re_path(r'^monitor/service', service.ResourcesConsumer),
        ])
    )
})
