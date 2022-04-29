from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class BaseModel(models.Model):
    """基类模型"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 抽象模型类, 用于继承使用


class Users(AbstractUser):
    """
    继承django的系统user
    """
    mobile = models.CharField(max_length=11, unique=True, null=True, blank=True, default=None, verbose_name='手机号码')
    image = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', blank=True, verbose_name='头像')
    # 用户与角色是多对多关系
    roles = models.ManyToManyField('Roles', db_table='oauth_users_to_oauth_roles', blank=True,
                                   verbose_name='角色')

    class Meta:
        db_table = 'oauth_users'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.username

    def _get_user_permissions(self):
        # 获取用户权限
        permissions = list(filter(None, set(self.roles.values_list('name', flat=True))))
        if 'admin' in permissions:
            permissions = ['admin']
        return permissions

    def get_user_info(self):
        # 获取用户信息
        user_info = {
            'id': self.pk,
            'username': self.username,
            'avatar': '/media/' + str(self.image),
            'email': self.email,
            'roles': self._get_user_permissions(),
            'mobile': '' if self.mobile is None else self.mobile
        }
        return user_info


class Permissions(BaseModel):
    """
    权限
    """
    method_choices = (
        (u'POST', u'增'),
        (u'DELETE', u'删'),
        (u'PUT', u'改'),
        (u'PATCH', u'局部改'),
        (u'GET', u'查')
    )

    name = models.CharField(max_length=30, verbose_name='权限名')
    method = models.CharField(max_length=8, blank=True, default='', choices=method_choices, verbose_name='方法')
    desc = models.CharField(max_length=30, blank=True, default='', verbose_name='权限描述')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'oauth_permissions'
        verbose_name = '权限'
        verbose_name_plural = verbose_name
        ordering = ['id']


class Roles(BaseModel):
    """
    角色
    """
    name = models.CharField(max_length=32, unique=True, verbose_name='角色')
    permissions = models.ManyToManyField('Permissions', db_table='oauth_roles_to_oauth_permissions',
                                         blank=True, verbose_name='权限')
    desc = models.CharField(max_length=50, blank=True, default='', verbose_name='描述')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'oauth_roles'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']
