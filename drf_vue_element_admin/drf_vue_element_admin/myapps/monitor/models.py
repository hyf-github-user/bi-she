from django.conf import settings
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    """基类模型"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        abstract = True  # 抽象模型类, 用于继承使用


class IpBlackList(BaseModel):
    """
    ip黑名单
    """
    ip = models.GenericIPAddressField(unique=True, verbose_name='IP')

    class Meta:
        db_table = 'monitor_ipblacklist'
        verbose_name = 'IP黑名单'
        verbose_name_plural = verbose_name
        ordering = ['-id']


class OnlineUsers(BaseModel):
    """
    在线用户
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='用户')
    ip = models.GenericIPAddressField(verbose_name='IP')

    class Meta:
        db_table = 'monitor_onlineusers'
        verbose_name = '在线用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']
