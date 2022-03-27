# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :__init__.py.py
# 时间    :2022/3/18 17:06
from rest_framework import serializers

from drf_vue_element_admin.myapps.blog.models import Post, Category, Comment, Link, Permission, Role, User, \
    Notification, Collect, RolesPermissions, Follow


class RoleSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Role  # 指定的模型类
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """
    # 多对一
    role = RoleSerializer()

    class Meta:
        model = User  # 指定的模型类
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Category  # 指定的模型类
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """
    # 多对一
    author = UserSerializer()
    # 多对一
    category = CategorySerializer()

    class Meta:
        model = Post  # 指定的模型类
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """
    # 多对一
    author = UserSerializer()
    post = PostSerializer()

    class Meta:
        model = Comment  # 指定的模型类
        fields = '__all__'


class CollectSerializer(serializers.ModelSerializer):
    # 一对一
    collector = UserSerializer()
    # 一对一
    collected = PostSerializer()

    class Meta:
        model = Collect  # 指定的模型类
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    # 一对一
    follower = UserSerializer()
    followed = UserSerializer()

    class Meta:
        model = Follow  # 指定的模型类
        fields = '__all__'


class LinkSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Link  # 指定的模型类
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Permission  # 指定的模型类
        fields = '__all__'


class NotificationSerializer(serializers.ModelSerializer):
    """
    前台通知的序列化器
    """
    # 多对一
    receiver = UserSerializer()

    class Meta:
        model = Notification  # 指定的模型类
        fields = '__all__'


class RolesPermissionsSerializer(serializers.ModelSerializer):
    # 一对一
    role = RoleSerializer()
    permission = PermissionSerializer()

    class Meta:
        model = RolesPermissions  # 指定的模型类
        fields = '__all__'
