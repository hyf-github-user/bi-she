from django.urls import path, include
from drf_vue_element_admin.myapps.monitor.views import users, service, ip
from drf_vue_element_admin.myapps.utils import routers

# 添加对IP操作的路由


router = routers.AdminRouter()
router.register(r'ip', ip.IpBlackListViewSet, basename="ip")  # ip黑名单管理
urlpatterns = [
    path('users/', users.OnlineUsersListAPIView.as_view()),  # 在线用户监控
    path('service/', service.ServiceMonitorAPIView.as_view()),  # 服务监控
    path('', include(router.urls)),
]
