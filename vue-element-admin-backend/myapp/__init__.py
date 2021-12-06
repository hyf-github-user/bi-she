# 作者：我只是代码的搬运工
# coding:utf-8
import click
from flask import Flask

from myapp.api.article import api_article
from myapp.api.comment import api_comment
from myapp.api.login import login_bp
from myapp.api.user import api_user
from myapp.blueprints.auth.views import auth_bp
from myapp.blueprints.user.views import user_bp
from exts import bootstrap, db, cors, dropzone, mail, avatars, login_manager
from myapp.models.user import Role, User

from settings import DevelopmentConfig


def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    # 初始化扩展
    register_extensions(app=app)
    # 注册蓝图
    register_blueprints(app=app)
    # # 数据库数据初始化
    # register_template_context(myapp=myapp)
    # 注册命令
    register_commands(app=app)
    # # 定义错误页面
    # register_errors(myapp=myapp)
    return app


def register_extensions(app):
    # 注册所有的扩展
    bootstrap.init_app(app=app)
    db.init_app(app=app)
    dropzone.init_app(app=app)
    login_manager.init_app(app=app)
    mail.init_app(app=app)
    avatars.init_app(app=app)
    # csrf.init_app(app=app)
    cors.init_app(app=app)


# 注册蓝图
def register_blueprints(app):
    # 注册api接口的路由
    app.register_blueprint(api_comment, url_prefix='/api')
    app.register_blueprint(api_user, url_prefix='/api')
    app.register_blueprint(api_article, url_prefix='/api')
    app.register_blueprint(login_bp, url_prefix='/api')
    # 前台蓝图注册
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(auth_bp, url_prefix='/auth')


# 绑定初始化命令
def register_commands(app):
    # 格式化系统数据库
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='格式化数据库')
    def initdb(drop):
        """
        格式化数据库
        :param drop:
        :return:
        """
        if drop:
            click.confirm("确认初始化数据库吗?", abort=True)
            db.drop_all()
            click.echo("格式化系统数据库完成!")
        db.create_all()
        click.echo("初始化系统数据库完成!")

    # 创建超级管理员的命令
    @app.cli.command()
    @click.option('--username', prompt=True, help='用户名用来登录')
    @click.option('--name', prompt=True, help='真实姓名')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='密码用来登录')
    def init(username, name, password):
        """
        创建超级管理员
        :param username:
        :param name:
        :param password:
        :return:
        """
        click.echo("开始创建超级管理员......")
        db.create_all()  # 根据模型生成相应的表
        click.echo('初始化权限与角色的数据库...')
        Role.init_role()
        admin = User.query.filter_by(auth=3).first()  # 首先查询是否存在超级管理员
        if admin is not None:
            click.echo('超级管理员账户已存在,正在更新管理员信息....')
            admin.username = username
            admin.set_password(password)
            admin.set_hash_password()  # 对哈希密码进行加密的密文
            admin.name = name
        else:
            click.echo('创建超级管理员账户中......')
            admin = User(
                username=username,
                auth=3,
                name=name,
                email=app.config['ADMIN_EMAIL'],
                confirmed=True,
                active=True
            )
            admin.set_password(password)
            admin.set_hash_password()  # 对哈希密码进行加密的密文
            db.session.add(admin)
            db.session.commit()
            click.echo("创建管理员成功!")

    # 创建测试员的命令
    @app.cli.command()
    @click.option('--test_username', prompt=True, help='用户名用来登录')
    @click.option('--test_name', prompt=True, help='真实姓名')
    @click.option('--test_email', prompt=True, help='QQ邮箱')
    @click.option('--test_password', prompt=False, hide_input=True,
                  confirmation_prompt=True, help='密码用来登录')
    def test(test_username, test_name, test_password, test_email):
        """
        测试
        :param test_username:
        :param test_name:
        :param test_password:
        :return:
        """
        test_password = "12345678"
        click.echo("开始创建测试员......")
        test_user = User.query.filter_by(username=test_username).first()  # 首先查询是否存在测试用户
        if test_user is not None:
            click.echo('测试账户已存在,正在更新测试员信息....')
            test_user.username = test_username
            test_user.set_password(test_password)
            test_user.set_hash_password()  # 对哈希密码进行加密的密文
            test_user.name = test_name
        else:
            click.echo('创建测试员账户中......')
            test_user = User(
                username=test_username,
                auth=1,
                name=test_name,
                email=test_email,
                confirmed=True,
                active=True
            )
            test_user.set_password(test_password)
            test_user.set_hash_password()  # 对哈希密码进行加密的密文
            db.session.add(test_user)
            db.session.commit()
            click.echo("创建测试员成功!")