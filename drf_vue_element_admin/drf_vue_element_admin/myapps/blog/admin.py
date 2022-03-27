from django.contrib import admin

from .models import User, Permission, Role, Post, Notification, Comment, Category, RolesPermissions, Link, Collect, \
    Follow

# Register your models here.
admin.site.register(User)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(Post)
admin.site.register(Notification)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(RolesPermissions)
admin.site.register(Collect)
admin.site.register(Link)
admin.site.register(Follow)
