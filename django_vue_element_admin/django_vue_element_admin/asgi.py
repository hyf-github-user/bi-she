# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :asgi.py
# 时间    :2022/3/14 07:20
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_vue_element_admin.settings')

application = get_asgi_application()
