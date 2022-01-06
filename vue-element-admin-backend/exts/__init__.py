# 作者：我只是代码的搬运工
# coding:utf-8
from flask_avatars import Avatars
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_login import LoginManager, AnonymousUserMixin
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_wtf import CSRFProtect

# 结合bootstrap
bootstrap = Bootstrap()
# 数据库的ORM模型
db = SQLAlchemy()
# 用户前后端交互
cors = CORS()
# 文件拖动上传扩展
dropzone = Dropzone()
# # 用于用户登录验证
login_manager = LoginManager()
# 用于发送QQ邮箱
mail = Mail()
# 头像插件
avatars = Avatars()


# 进行CSRF保护
# csrf = CSRFProtect()


# 把user存入Session中


@login_manager.user_loader
def load_user(user_id):
    from myapp.models.user import User
    user = User.query.get(int(user_id))  # 把当前的用户存入Session中
    return user


# 用户加载函数,判断当前是否登录,用于current_user
login_manager.login_view = 'auth.login'  # 未登录时进入这个路由
login_manager.login_message = '请先登录!'  # 未登录弹出的消息
login_manager.login_message_category = 'warning'  # 未登录时弹出消息的类别

# 当修改密码时刷新登录
login_manager.refresh_view = 'auth.re_authenticate'  # 刷新登录时进入的路由
login_manager.needs_refresh_message = '为了保护你的账户,请重新刷新进入这个页面!'  # 刷新时弹出的消息
login_manager.needs_refresh_message_category = 'warning'  # 刷新时弹出消息的类别


# 设置匿名用户(就是访客的)模型
class Guest(AnonymousUserMixin):
    # 访客没有啥权限
    def can(self, permission_name):
        return False

    # 访客更不可能是管理员
    @property
    def is_admin(self):
        return False


# 匿名用户设置
login_manager.anonymous_user = Guest
