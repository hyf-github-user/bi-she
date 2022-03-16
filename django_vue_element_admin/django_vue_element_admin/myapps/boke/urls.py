# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :urls.py
# 时间    :2022/3/15 10:37

from rest_framework import routers
from django_vue_element_admin.myapps.boke.views import CategoryViewSet, CommentViewSet, LinkViewSet, PermissionViewSet, \
    PostViewSet, RoleViewSet, UserViewSet

urlpatterns = [

]
router = routers.DefaultRouter()
# 注册用户视图
router.register(r'users', UserViewSet, basename='user')
router.register(r'role', RoleViewSet, basename='role')
router.register(r'post', PostViewSet, basename='post')
router.register(r'permission', PermissionViewSet, basename='permission')
router.register(r'link', LinkViewSet, basename='link')
router.register(r'comment', CommentViewSet, basename='comment')
router.register(r'category', CategoryViewSet, basename='category')
urlpatterns += router.urls
