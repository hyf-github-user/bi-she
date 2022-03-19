from rest_framework import routers

from drf_vue_element_admin.myapps.blog.views import UserViewSet, RoleViewSet, PostViewSet, PermissionViewSet, \
    LinkViewSet, CommentViewSet, CategoryViewSet, NotificationViewSet

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
router.register(r'notification', NotificationViewSet, basename='notification')
urlpatterns += router.urls
