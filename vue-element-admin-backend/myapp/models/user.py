# 作者：我只是代码的搬运工
# coding:utf-8
from datetime import datetime
from flask import current_app
from flask_avatars import Identicon
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from exts import db, whooshee


# 用户与用户关联模型(自我关联模型)
class Follow(db.Model):
    # 自我关联关系, joined表示和父查询一样加载记录,但使用联结,foreign_keys可以让外键找到对应外键,follower->follower_id,followed->followed_id
    # 关注者的id
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    follower = db.relationship('User', foreign_keys=[follower_id], back_populates='following', lazy='joined')
    # 被关注的人的id
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                            primary_key=True)
    followed = db.relationship('User', foreign_keys=[followed_id], back_populates='followers', lazy='joined')

    # 关注的时间
    timestamp = db.Column(db.DateTime, default=datetime.now)


@whooshee.register_model('name', 'username')
class User(db.Model, UserMixin):
    """
        用户表模型
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False)  # 登录名称
    password_hash = db.Column(db.String(120))  # 哈希密码
    name = db.Column(db.String(20), nullable=False)  # 真实姓名
    email = db.Column(db.String(254), nullable=False,
                      unique=True, index=True)  # 用户邮箱
    website = db.Column(db.String(255))  # 个人网站
    register_time = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    # 个人头像三种类型(s m l)
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    # 专门存放裁剪的头像
    avatar_raw = db.Column(db.String(64))
    # 存放登录密码
    private_key = db.Column(db.Text(), comment="加密密码的私钥")
    rsa_password = db.Column(db.Text(), comment="对密码进行加密之后的密文")
    # 用户状态
    active = db.Column(db.Boolean, default=True)  # 是否激活用户
    confirmed = db.Column(db.Boolean, default=False)  # 确认注册

    # 身份字段
    # 用户与身份的关联(一对多)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), default=2)
    role = db.relationship('Role', back_populates='users')

    # 是否接收通知消息
    receive_comment_notification = db.Column(db.Boolean, default=True)
    receive_follow_notification = db.Column(db.Boolean, default=True)
    receive_collect_notification = db.Column(db.Boolean, default=True)

    # User与Notification的一对多关系模型,cascade=all当用户删除时,所对应的所有的notification全部要删除
    notifications = db.relationship('Notification', back_populates='receiver', cascade='all')
    # 用户与评论是一对多的关系
    comments = db.relationship('Comment', back_populates='author', cascade='all')

    # 用户与文章是一对多的关系
    posts = db.relationship('Post', back_populates='author', cascade='all')

    # User与collect的一对多模型
    collections = db.relationship('Collect', back_populates='collector',
                                  cascade='all')  # cascade='all' 指的是当用户删除后,对应的collect就会被删掉
    # 是否公开收藏
    public_collections = db.Column(db.Boolean, default=False)

    # 所有我关注的人, foreign_keys指定反向属性,foreign_keys可以让外键找到对应外键,follower->follower_id,followed->followed_id
    following = db.relationship('Follow', foreign_keys=[Follow.follower_id], back_populates='follower',
                                lazy='dynamic', cascade='all')
    # 所有我的粉丝
    followers = db.relationship('Follow', foreign_keys=[Follow.followed_id], back_populates='followed',
                                lazy='dynamic', cascade='all')

    # 创建构造函数
    def __init__(self, **kwargs):
        # 对父类的所有属性与方法进行调用
        super(User, self).__init__(**kwargs)
        self.set_role()  # 调用生成角色方法
        self.set_private_key()  # 生成私钥与保存公钥
        # 自定义生成头像
        self.generate_avatar()
        # 用户关注自己
        self.follow(self)

    # 初始化角色信息,设置role
    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='admin').first()
            else:
                self.role = Role.query.filter_by(name='user').first()
            db.session.commit()

    # 设置密码
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)  # 生成哈希加密的密码
        # 对真实密码进行rsa加密
        from myapp.utils.rsa_message import RSAUtil, BytesToHexStr
        # 对密码加密之后的密文
        self.rsa_password = BytesToHexStr(RSAUtil.encrypt(
            RSAUtil.getPublicKey(self.id), password))

    # 设置公钥与私钥
    def set_private_key(self):
        from myapp.utils.rsa_message import RSAUtil, BytesToHexStr
        self.private_key = BytesToHexStr(
            RSAUtil.create_keys(self.id))  # 保存私钥,与公钥

    # 验证密码
    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    # 自动生成头像
    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    # 一个方法变成属性调用
    @property
    def is_admin(self):
        return self.role.name == 'admin'

    # 验证是否被激活了
    @property
    def is_active(self):
        return self.active

    # 验证权限验证的方法,参数就是权限的名称进行验证
    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions

    # 关注用户行为
    def follow(self, user):
        # 判断是否关注它
        if not self.is_following(user):
            # 关注它
            follow = Follow(follower=self, followed=user)
            db.session.add(follow)
            db.session.commit()

    # 取消关注某人
    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)
            db.session.commit()

    # 查看此用户有无关注这个用户
    def is_following(self, user):
        if user.id is None:  # when follow self, user.id will be None
            return False
        return self.following.filter_by(followed_id=user.id).first() is not None

    # 查找自己关注了别人
    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).first() is not None

    # 收藏图片方法
    def collect(self, post):
        collect = Collect(collector=self, collected=post)
        db.session.add(collect)
        db.session.commit()

    # 取消收藏文章
    def uncollect(self, post):
        # 根据user查询对应的collect
        collect = Collect.query.with_parent(self).filter_by(collected_id=post.id).first()
        if collect:
            db.session.delete(collect)
            db.session.commit()

    # 查找用户有无收藏此文章
    def is_collecting(self, post):
        return Collect.query.with_parent(self).filter_by(collected_id=post.id).first() is not None


# 权限与角色的关联表(多对多)
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer,
                                       db.ForeignKey('role.id'), primary_key=True),
                             db.Column('permission_id', db.Integer,
                                       db.ForeignKey('permission.id'), primary_key=True)
                             )


# 用户身份表
class Role(db.Model):
    """
    用户身份表
    """
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 主键
    name = db.Column(db.String(30), unique=True,
                     nullable=False, default="user")  # 身份描述(四种)
    description = db.Column(db.String(255))  # 身份描述
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    # 关系属性
    # 一对多的关系属性 身份与用户是一对多模型
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship(
        'Permission', secondary=roles_permissions, back_populates='roles')  # 多对多的模型联系

    # 初始化角色的静态方法,创建各种角色
    @staticmethod
    def init_role():
        # 各个身份的权限
        roles_permissions_map = {
            'locked': ['FOLLOW', 'COLLECT'],
            'user': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],
            'admin': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']
        }
        # 遍历权限列表,创建各种身份,四种身份
        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            # 遍历权限功能,并创建相应的权限
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(
                    name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()


# 权限功能表
class Permission(db.Model):
    __tablename__ = "permission"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30), unique=True)  # 存储权限功能说明
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    description = db.Column(db.String(255))  # 身份描述
    roles = db.relationship(
        'Role', secondary=roles_permissions, back_populates='permissions')  # 多对多的模型联系


@whooshee.register_model('title')
class Post(db.Model):
    """
    文章模型
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="文章主键")
    # 文章主题
    title = db.Column(db.String(255))
    # 文章内容
    body = db.Column(db.Text)
    # 文章创建时间
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    # 文章是否能被评论
    can_comment = db.Column(db.Boolean, default=True)  # 是否能评论
    # 文章重要性
    importance = db.Column(db.SmallInteger, default=1, comment="重要性")
    # 文章的状态
    status = db.Column(db.String(255), default='published')
    # 标记被举报的次数
    flag = db.Column(db.Integer, default=0, comment="文章被举报次数")
    # 分类与文章一对多对多的关系属性
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')
    # 文章与评论是一对多的关系
    comments = db.relationship('Comment', back_populates='post', cascade='all')
    # 用户与文章是一对多的关系
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')
    # Post与collect的一对多模型
    collectors = db.relationship('Collect', back_populates='collected',
                                 cascade='all')  # cascade='all' 指的是当文章删除后,对应的collect就会被删掉


# 收藏表(),使用关联模型把User与Post的多对多模型给分离成一对多模型
class Collect(db.Model):
    collector_id = db.Column(db.Integer, db.ForeignKey('user.id'),  # 收藏文章人的ID  与User形成一对多模型
                             primary_key=True)
    collected_id = db.Column(db.Integer, db.ForeignKey('post.id'),  # 被用户收藏文章ID  与Post形成一对多模型
                             primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)  # 收藏时间

    collector = db.relationship('User', back_populates='collections', lazy='joined')  # 收藏人(一对多) 对应User
    collected = db.relationship('Post', back_populates='collectors', lazy='joined')  # 被收藏的文章(一对多)  对应Post


class Category(db.Model):
    """
    文章分类
    """
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="分类主键")
    # 分类名称,index是为了方便索引
    name = db.Column(db.String(64), index=True, unique=True)
    # 分类创建时间
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)

    # 关系属性,分类与文章是一对多的关系
    posts = db.relationship('Post', back_populates='category')


class Comment(db.Model):
    """
    评论模型
    """
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="评论主键")
    body = db.Column(db.Text)
    # 评论创建时间
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    # 标记被举报的次数
    flag = db.Column(db.Integer, default=0, comment="评论被举报次数")
    # 用户与评论是一对多的关系
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='comments')
    # 文章与评论是一对多的关系
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))
    post = db.relationship('Post', back_populates='comments')

    reviewed = db.Column(db.Boolean, default=False, comment="是否通过审核")  # 判断是否通过审核
    # 回复评论
    # 评论被回复的评论id,一个评论与回复是一对多的关系
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 被回复的评论的关系属性,remote_side是关系的远程侧,指的是回复的评论id
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])

    # 评论文章的评论的关系属性
    replies = db.relationship('Comment', back_populates='replied', cascade='all')


class Link(db.Model):
    """
    友情链接
    """
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(30))
    url = db.Column(db.String(255))
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)


class Notification(db.Model):
    """
    用户通知模型
    """
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    # 是否已读
    is_read = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    # User与Notification的一对多关系
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    receiver = db.relationship('User', back_populates='notifications')
