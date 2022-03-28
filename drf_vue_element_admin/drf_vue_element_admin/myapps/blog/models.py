from django.db import models

# Create your models here.
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(unique=True, max_length=64, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'category'
        ordering = ['id']


class Collect(models.Model):
    collector = models.OneToOneField('User', models.DO_NOTHING, primary_key=True)
    collected = models.OneToOneField('Post', models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.collector.username + "收藏了" + self.collected.title

    class Meta:
        db_table = 'collect'
        unique_together = (('collector', 'collected'),)
        ordering = ['collector']


class Comment(models.Model):
    body = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, default=timezone.now)
    flag = models.IntegerField(blank=True, null=True, default=0)
    author = models.ForeignKey('User', models.DO_NOTHING, blank=True)
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True)
    reviewed = models.IntegerField(blank=True, default=0)
    replied = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    # def __str__(self):
    #     return self.author.username + "的评论"

    class Meta:
        db_table = 'comment'
        ordering = ['id']


class Follow(models.Model):
    follower = models.OneToOneField('User', models.DO_NOTHING, primary_key=True, related_name="follower")
    followed = models.OneToOneField('User', models.DO_NOTHING, related_name='followed')
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.follower.username + "关注了" + self.followed.username

    class Meta:
        db_table = 'follow'
        unique_together = (('follower', 'followed'),)
        ordering = ['follower']


class Link(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'link'
        ordering = ['id']


class Notification(models.Model):
    message = models.TextField()
    is_read = models.IntegerField(blank=True, default=0)
    timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    receiver = models.ForeignKey('User', models.DO_NOTHING, blank=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'notification'
        ordering = ['id']


class Permission(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'permission'
        ordering = ['id']


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True)
    body = models.TextField(blank=True)
    timestamp = models.DateTimeField(blank=True, null=True, default=timezone.now)
    can_comment = models.IntegerField(blank=True, null=True, default=1)
    importance = models.IntegerField(blank=True, null=True, default=1)
    status = models.CharField(max_length=255, blank=True, null=True, default="draft")
    flag = models.IntegerField(blank=True, null=True, default=0)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True)
    author = models.ForeignKey('User', models.DO_NOTHING, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'post'
        ordering = ['id']


class Role(models.Model):
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    permissions = models.ManyToManyField('Permission', through='RolesPermissions',
                                         blank=True, verbose_name='权限')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'role'
        ordering = ['id']


class RolesPermissions(models.Model):
    role = models.OneToOneField('Role', models.DO_NOTHING, primary_key=True)
    permission = models.OneToOneField('Permission', models.DO_NOTHING)

    def __str__(self):
        return self.role.name + "的权限: " + self.permission.name

    class Meta:
        db_table = 'roles_permissions'
        unique_together = (('role', 'permission'),)
        ordering = ['role']


class User(models.Model):
    username = models.CharField(max_length=120)
    password_hash = models.CharField(max_length=120, blank=True, null=True)
    auth = models.SmallIntegerField(blank=True, null=True)
    name = models.CharField(max_length=20)
    email = models.CharField(unique=True, max_length=254)
    website = models.CharField(max_length=255, blank=True, null=True)
    register_time = models.DateTimeField(blank=True, null=True)
    avatar_s = models.CharField(max_length=64, blank=True, null=True)
    avatar_m = models.CharField(max_length=64, blank=True, null=True)
    avatar_l = models.CharField(max_length=64, blank=True, null=True)
    avatar_raw = models.CharField(max_length=64, blank=True, null=True)
    private_key = models.TextField(blank=True, null=True)
    rsa_password = models.TextField(blank=True, null=True)
    active = models.IntegerField(blank=True, null=True)
    confirmed = models.IntegerField(blank=True, null=True)
    locked = models.IntegerField(blank=True, null=True)
    role = models.ForeignKey(Role, models.DO_NOTHING, blank=True, null=True)
    receive_comment_notification = models.IntegerField(blank=True, null=True)
    receive_follow_notification = models.IntegerField(blank=True, null=True)
    receive_collect_notification = models.IntegerField(blank=True, null=True)
    public_collections = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'
        ordering = ['id']
