# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :__init__.py.py
# 时间    :2022/3/18 17:20
from django_redis import get_redis_connection
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from drf_vue_element_admin.myapps.blog.models import Post, Comment, User, Permission, Link, Category, Notification, Role
from drf_vue_element_admin.myapps.blog.serializers import RoleSerializer, UserSerializer, PostSerializer, \
    CategorySerializer, CommentSerializer, PermissionSerializer, LinkSerializer, NotificationSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # 根据用户的username进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('username',)


class RoleViewSet(ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    # 根据角色的name进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # 根据文章title进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('title',)


class PermissionViewSet(ModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    # 根据权限name进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class LinkViewSet(ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer
    # 提供根据name进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class CommentViewSet(ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # 提供根据评论作者username进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('author.username',)


class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # 根据的分类名进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('name',)


class NotificationViewSet(ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    # 提供根据通知接收者的username进行查找
    filter_backends = (SearchFilter,)
    search_fields = ('receiver.username',)


class BlogDataView(APIView):

    def get(self, request):
        # 获取通知总数
        notifications = Notification.objects.all().count()
        # 获取评论总数
        comments = Comment.objects.all().count()
        # 获取用户总数
        users = User.objects.all().count()
        # 获取文章总数
        posts = Post.objects.all().count()

        # 流量
        conn = get_redis_connection('user_info')
        visits = conn.get('visits')

        return Response(data={'notifications': notifications, 'comments': comments, 'users': users, 'posts': posts,
                              'visits': visits})
