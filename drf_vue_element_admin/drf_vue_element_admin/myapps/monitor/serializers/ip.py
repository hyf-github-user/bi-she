from rest_framework import serializers

from drf_vue_element_admin.myapps.monitor.models import IpBlackList


class IpBlackListSerializer(serializers.ModelSerializer):
    """
    IP黑名单管理序列化器
    """
    create_time = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = IpBlackList
        fields = '__all__'
