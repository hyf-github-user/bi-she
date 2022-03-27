# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AlembicVersion(models.Model):
    version_num = models.CharField(primary_key=True, max_length=32)

    class Meta:
        managed = False
        db_table = 'alembic_version'


class Category(models.Model):
    name = models.CharField(unique=True, max_length=64, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'category'


class Collect(models.Model):
    collector = models.ForeignKey('User', models.DO_NOTHING, primary_key=True)
    collected = models.ForeignKey('Post', models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'collect'
        unique_together = (('collector', 'collected'),)


class Comment(models.Model):
    body = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    author = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    post = models.ForeignKey('Post', models.DO_NOTHING, blank=True, null=True)
    reviewed = models.IntegerField(blank=True, null=True)
    replied = models.ForeignKey('self', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'comment'


class Follow(models.Model):
    follower = models.ForeignKey('User', models.DO_NOTHING, primary_key=True)
    followed = models.ForeignKey('User', models.DO_NOTHING)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'follow'
        unique_together = (('follower', 'followed'),)


class Link(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'link'


class Notification(models.Model):
    message = models.TextField()
    is_read = models.IntegerField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    receiver = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notification'


class Permission(models.Model):
    name = models.CharField(unique=True, max_length=30, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'permission'


class Post(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    can_comment = models.IntegerField(blank=True, null=True)
    importance = models.SmallIntegerField(blank=True, null=True)
    status = models.CharField(max_length=255, blank=True, null=True)
    flag = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    author = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'post'


class Role(models.Model):
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'role'


class RolesPermissions(models.Model):
    role = models.ForeignKey(Role, models.DO_NOTHING, primary_key=True)
    permission = models.ForeignKey(Permission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'roles_permissions'
        unique_together = (('role', 'permission'),)


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

    class Meta:
        managed = False
        db_table = 'user'
