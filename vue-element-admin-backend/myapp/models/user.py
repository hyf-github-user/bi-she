# 作者：我只是代码的搬运工
# coding:utf-8
from datetime import datetime
from flask import current_app
from flask_avatars import Identicon
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash
from exts import db
from myapp.utils.network import Result


class User(db.Model, UserMixin):
    """
        用户表模型
    """
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(120), nullable=False)  # 登录名称
    password_hash = db.Column(db.String(120))  # 哈希密码
    auth = db.Column(db.SmallInteger, default=1)  # 级别(分为1,2,3 三个等级)
    name = db.Column(db.String(20), nullable=False)  # 真实姓名
    email = db.Column(db.String(254), nullable=False,
                      unique=True, index=True)  # 用户邮箱
    website = db.Column(db.String(255))  # 个人网站
    register_time = db.Column(db.DateTime, default=datetime.now)  # 注册时间
    # 个人头像三种类型(s m l)
    avatar_s = db.Column(db.String(64))
    avatar_m = db.Column(db.String(64))
    avatar_l = db.Column(db.String(64))
    # 存放登录密码
    private_key = db.Column(db.Text(), comment="加密密码的私钥")
    rsa_password = db.Column(db.Text(), comment="对密码进行加密之后的密文")
    # 用户状态
    active = db.Column(db.Boolean, default=True)  # 是否激活用户
    confirmed = db.Column(db.Boolean, default=False)  # 确认注册
    locked = db.Column(db.Boolean, default=False)  # 锁定用户

    # 身份字段
    # 用户与身份的关联(一对多)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    role = db.relationship('Role', back_populates='users')

    # 用户与评论是一对多的关系
    comments = db.relationship('Comment', back_populates='author', cascade='all')

    # 用户与文章是一对多的关系
    posts = db.relationship('Post', back_populates='author', cascade='all')

    # 创建构造函数
    def __init__(self, **kwargs):
        # 对父类的所有属性与方法进行调用
        super(User, self).__init__(**kwargs)
        self.set_role()  # 调用生成角色方法
        self.set_private_key()  # 生成私钥与保存公钥
        # 自定义生成头像
        self.generate_avatar()

    # 更新用户信息
    def update(self, username, name, email, active, locked, confirmed, role_id):
        self.username = username
        self.name = name
        self.email = email
        self.active = active
        self.confirmed = confirmed
        self.role_id = role_id
        # role_id与locked的关系
        if self.role_id == 1:
            self.locked = 1
        else:
            self.locked = locked
        if self.locked == 1:
            self.role_id = 1
            self.auth = 1
        else:
            # 保证auth与role_id一样
            self.auth = self.role_id

    # 转换为json数据
    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'name': self.name,
            'auth': self.auth,
            'email': self.email,
            'active': self.active,
            'confirmed': self.confirmed,
            'locked': self.locked,
            'register_time': self.register_time,
            'rsa_password_hash': self.rsa_password,
            'role_id': self.role_id,
        }

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

    # 验证rsa密码
    def check_rsa(self, password):
        pass

    # 自动生成头像
    def generate_avatar(self):
        avatar = Identicon()
        filenames = avatar.generate(text=self.username)
        self.avatar_s = filenames[0]
        self.avatar_m = filenames[1]
        self.avatar_l = filenames[2]
        db.session.commit()

    # 验证密码
    @staticmethod
    def verify(username, password):
        user = User.query.filter_by(username=username).first()
        if not user:  # 无用户
            # 返回认证失败的错误
            return Result.error(message="无此用户!"), False
        if not user.check_password(password):  # 密码错误
            return Result.error(message="用户名或密码错误!"), False
        # 用户类别判断
        scope = 'admin' if user.auth == 4 else \
            'editor' if user.auth == 3 \
                else 'user'
        return {'uid': user.id, 'scope': scope}, True

    # 产生token
    @staticmethod
    def create_token(uid, scope):
        s = Serializer(current_app.config['JWT_SECRET'], expires_in=current_app.config['TOKEN_EXPIRATION'])
        t = s.dumps({
            'uid': uid,
            'scope': scope
        })
        # 进行ASCII编码
        token = {
            'token': t.decode('ascii')
        }
        return token

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


# 权限与角色的关联表(多对多)
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer,
                                       db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer,
                                       db.ForeignKey('permission.id'))
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
            'editor': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],
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
    roles = db.relationship(
        'Role', secondary=roles_permissions, back_populates='permissions')  # 多对多的模型联系


# 文章与分类是多对多模型,采用了中间表的关系描述
post_category = db.Table('post_category',
                         db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
                         db.Column('category_id', db.ForeignKey('category.id')))


class Post(db.Model):
    """
    文章模型
    """
    __tablename__ = "post"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment="文章主键")
    # 文章主题
    title = db.Column(db.String(255))
    # 文章内容,属于markdown的文件
    body = db.Column(db.Text)
    # markdown渲染之后的html文件
    body_html = db.Column(db.Text)
    # 文章创建时间
    timestamp = db.Column(db.DateTime, default=datetime.now, index=True)
    # 文章是否能被评论
    can_comment = db.Column(db.Boolean, default=True)  # 是否能评论
    # 标记被举报的次数
    flag = db.Column(db.Integer, default=0, comment="文章被举报次数")
    # 文章与分类多对多的关系属性
    categories = db.relationship('Category', secondary=post_category, back_populates='posts')
    # 文章与评论是一对多的关系
    comments = db.relationship('Comment', back_populates='post', cascade='all')
    # 用户与文章是一对多的关系
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    author = db.relationship('User', back_populates='posts')


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

    # 关系属性
    posts = db.relationship('Post', secondary=post_category, back_populates='categories')


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

    # 回复评论
    # 评论被回复的评论id,一个评论与回复是一对多的关系
    replied_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    # 被回复的评论的关系属性,remote_side是关系的远程侧,指的是回复的评论id
    replied = db.relationship('Comment', back_populates='replies', remote_side=[id])

    # 评论文章的评论的关系属性
    replies = db.relationship('Comment', back_populates='replied', cascade='all')
