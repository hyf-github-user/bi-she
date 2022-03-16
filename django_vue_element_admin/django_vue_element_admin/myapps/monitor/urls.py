from django.urls import path, include
from django_vue_element_admin.myapps.utils import routers

from django_vue_element_admin.myapps.monitor.views import service, users, error, crud, ip

# 添加对IP操作的路由
router = routers.AdminRouter()
router.register(r'ip', ip.IpBlackListViewSet, basename="ip")  # ip黑名单管理
urlpatterns = [
    path('users/', users.OnlineUsersListAPIView.as_view()),  # 在线用户监控
    path('service/', service.ServiceMonitorAPIView.as_view()),  # 服务监控
    path('error/', error.ErrorLogAPIView.as_view()),  # 错误日志监控
    path('crud/', crud.CRUDListAPIView.as_view()),  # CRUD变更记录
    path('', include(router.urls)),
]
