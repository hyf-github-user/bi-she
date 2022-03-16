from django.contrib import admin
from django.contrib.auth import get_user_model
from django_vue_element_admin.myapps.system.models import Permissions, Roles, Departments

# Register your test_model here.


Users = get_user_model()

# 注册模型到Django的后台管理
admin.site.register(Users)
admin.site.register(Permissions)
admin.site.register(Roles)
admin.site.register(Departments)

