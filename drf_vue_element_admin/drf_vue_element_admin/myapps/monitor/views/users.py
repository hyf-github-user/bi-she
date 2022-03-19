from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView

from drf_vue_element_admin.myapps.monitor.models import OnlineUsers
from drf_vue_element_admin.myapps.monitor.serializers.users import OnlineUsersSerializer


class OnlineUsersListAPIView(ListAPIView):
    """
    get:
    监控--在线用户

    获取在线用户信息, status: 200(成功), return: 在线用户信息
    """

    queryset = OnlineUsers.objects.all()
    serializer_class = OnlineUsersSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('username', 'ip')
