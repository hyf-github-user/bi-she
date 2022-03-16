from django.contrib import admin
from django_vue_element_admin.myapps.boke.models import User, Category, Collect, Comment, Follow, Link, Notification, Permission, Post, Role, \
    RolesPermissions

# Register your test_model here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Collect)
admin.site.register(Comment)
admin.site.register(Follow)
admin.site.register(Link)
admin.site.register(Notification)
admin.site.register(Permission)
admin.site.register(Post)
admin.site.register(Role)
admin.site.register(RolesPermissions)
