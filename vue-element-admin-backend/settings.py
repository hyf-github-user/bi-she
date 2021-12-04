# 作者：我只是代码的搬运工
# coding:utf-8
import os

basedir = os.path.dirname(__file__)
RAS_PATH = f'{basedir}/rsa/'


class BaseConfig(object):
    # session加密
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    TOKEN_EXPIRATION = 30 * 24 * 3600  # 令牌过期时间
    # 配置数据库连接
    # mysql + pymysql://user:password@hostip:port/数据名称
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hu15879093053@localhost:3306/grad_pro'
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # True时会追踪对象修改并且发送信号,需要额外的内存
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', '1348977728@qq.com')


# 俩种配置
class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
