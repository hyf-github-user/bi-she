# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :__init__.py.py
# 时间    :2022/3/18 17:06
from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegSerializer(serializers.ModelSerializer):
    """
    注册用户时的序列化器
    """

    def create(self, validated_data):
        """
        自定义创建用户方法
        :param validated_data:
        :return:
        """
        user = super(UserRegSerializer, self).create(validated_data=validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['username', 'mobile', 'password', 'roles', 'image']


class UserSerializer(serializers.ModelSerializer):
    roles_list = serializers.SerializerMethodField()
    is_superuser = serializers.BooleanField(read_only=True)

    def get_roles_list(self, obj):
        return [{'id': role.id, 'desc': role.desc} for role in obj.roles.all()]

    class Meta:
        model = User
        fields = ['id', 'username', 'mobile', 'email',
                  'roles', 'roles_list', 'is_superuser']
