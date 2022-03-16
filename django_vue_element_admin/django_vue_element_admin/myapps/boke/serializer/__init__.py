# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :__init__.py.py
# 时间    :2022/3/15 12:51
from rest_framework import serializers

from django_vue_element_admin.myapps.boke.models import Category, Comment, Link, User, Post, Role, Permission


class CategorySerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Category  # 指定的模型类
        fields = '__all__'


class CommentSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Comment  # 指定的模型类
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


class PostSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Post  # 指定的模型类
        fields = '__all__'


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

    class Meta:
        model = User  # 指定的模型类
        fields = '__all__'
