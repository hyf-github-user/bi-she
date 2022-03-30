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
    permissions = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Role  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'permissions': {
                'read_only': True,
            },
        }


class RolesPartialSerializer(serializers.ModelSerializer):
    """
    用户局部更新序列化器(角色授权)
    """

    class Meta:
        model = Role
        fields = ['id', 'permissions']


class UserSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    # 返回role的ID
    # role = serializers.PrimaryKeyRelatedField()
    roles_list = serializers.SerializerMethodField(read_only=True)

    # 返回关联属性的多个字段
    # role = RoleSerializer()
    # 调用role的str方法,一对一
    # role = serializers.StringRelatedField()

    def get_roles_list(self, obj):
        # 获取用户角色列表
        return {'id': obj.role.id, 'name': obj.role.name, 'description': obj.role.description}

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
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class PostSerializer(serializers.ModelSerializer):
    """
    前台文章的序列化器
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
    # 返回关联属性的post的str方法,read_only表示只参与序列化不参与反序列化
    post = serializers.StringRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class CollectSerializer(serializers.ModelSerializer):
    # 一对一
    collector = UserSerializer(read_only=True)
    # 一对一
    collected = PostSerializer(read_only=True)

    class Meta:
        model = Collect  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class FollowSerializer(serializers.ModelSerializer):
    # 一对一
    follower = UserSerializer(read_only=True)
    followed = UserSerializer(read_only=True)

    class Meta:
        model = Follow  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class LinkSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Link  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class PermissionSerializer(serializers.ModelSerializer):
    """
    前台用户的序列化器
    """

    class Meta:
        model = Permission  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class NotificationSerializer(serializers.ModelSerializer):
    """
    前台通知的序列化器
    """
    # 多对一

    receiver_list = serializers.SerializerMethodField(read_only=True)

    #
    def get_receiver_list(self, obj):
        # 获取通知者
        return {'id': obj.receiver.id, "username": obj.receiver.username}

    class Meta:
        model = Notification  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }


class RolesPermissionsSerializer(serializers.ModelSerializer):
    # 一对一
    role = RoleSerializer()
    permission = PermissionSerializer()

    class Meta:
        model = RolesPermissions  # 指定的模型类
        fields = '__all__'
        extra_kwargs = {
            'timestamp': {
                'read_only': True,
            },
        }
