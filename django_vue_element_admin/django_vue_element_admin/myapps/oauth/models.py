from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your test_model here.
class Users(AbstractUser):
    """
    继承django的系统user
    """
    name = models.CharField(max_length=20, default='', blank=True, verbose_name='真实姓名')
    mobile = models.CharField(max_length=11, unique=True, null=True, blank=True, default=None, verbose_name='手机号码')
    image = models.ImageField(upload_to='avatar/%Y/%m', default='avatar/default.png', blank=True, verbose_name='头像')
    # 用户与角色是多对多关系
    roles = models.ManyToManyField('system.Roles', db_table='oauth_users_to_system_roles', blank=True,
                                   verbose_name='角色')
    # 部门与用户是一对多关系
    department = models.ForeignKey('system.Departments', null=True, blank=True, on_delete=models.SET_NULL,
                                   verbose_name='部门')

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
            'name': self.name,
            'avatar': '/media/' + str(self.image),
            'email': self.email,
            'roles': self._get_user_permissions(),
            'department': self.department.name if self.department else '',
            'mobile': '' if self.mobile is None else self.mobile
        }
        return user_info
