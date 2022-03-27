from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Permissions, Roles
from django.contrib.auth.admin import UserAdmin

Users = get_user_model()
# Register your models here.
admin.site.register(Users, UserAdmin)
admin.site.register(Permissions)
admin.site.register(Roles)
