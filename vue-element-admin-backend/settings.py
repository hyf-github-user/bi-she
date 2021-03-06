# 作者：我只是代码的搬运工
# coding:utf-8
import os

basedir = os.path.dirname(__file__)
RAS_PATH = f'{basedir}/rsa_pubkey/'


# 保存三种的变量
class Operations:
    CONFIRM = 'confirm'  # 确认注册操作
    RESET_PASSWORD = 'reset-password'  # 重置密码的操作
    CHANGE_EMAIL = 'change-email'  # 修改邮箱的操作


class BaseConfig(object):
    # 上传文件的保存路径
    BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    if not os.path.exists(BLUELOG_UPLOAD_PATH):
        os.makedirs(BLUELOG_UPLOAD_PATH)
    # session加密
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev key')
    TOKEN_EXPIRATION = 100000  # 令牌过期时间
    JWT_SECRET = "safasfasfas"
    # 配置数据库连接
    # mysql + pymysql://user:password@hostip:port/数据名称
    DATABASE_USER = os.getenv('DATABASE_USER', 'root')
    DATABASE_PWD = os.getenv('DATABASE_PWD', 'hu15879093053')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'grad_pro')
    DATABASE_HOST = os.getenv('DATABASE_HOST', '127.0.0.1')
    DATABASE_PORT = os.getenv('DATABASE_PORT', '3306')
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(DATABASE_USER, DATABASE_PWD, DATABASE_HOST,
                                                                      DATABASE_PORT, DATABASE_NAME)
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # True时会追踪对象修改并且发送信号,需要额外的内存
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', '1348977728@qq.com')
    # 配置邮箱
    BLUELOG_MAIL_SUBJECT_PREFIX = '[Bluelog]'
    MAIL_DEBUG = True  # 开启debug，便于调试看信息
    MAIL_SUPPRESS_SEND = False  # 发送邮件，为True则不发送
    MAIL_SERVER = 'smtp.qq.com'  # 电子邮件服务器的主机名或IP地址
    MAIL_PORT = 465  # 电子邮件服务器的端口
    MAIL_USE_TLS = False  # 启用传输层安全协议
    MAIL_USE_SSL = True  # 启用安全套接层协议
    MAIL_USERNAME = '1348977728@qq.com'  # 邮件账户用户名
    MAIL_PASSWORD = 'tqekpctqcoxkffeg'  # 邮件账户的密码
    MAIL_DEFAULT_SENDER = '1348977728@qq.com'  # 填邮箱，默认发送者
    # 设置头像的配置
    AVATARS_SAVE_PATH = os.path.join(BLUELOG_UPLOAD_PATH, 'avatars')
    if not os.path.exists(AVATARS_SAVE_PATH):
        os.makedirs(AVATARS_SAVE_PATH)
    AVATARS_SIZE_TUPLE = (30, 100, 200)
    # 上传图片保存的位置
    PHOTO_SAVE_PATH = os.path.join(BLUELOG_UPLOAD_PATH, 'photos')
    if not os.path.exists(PHOTO_SAVE_PATH):
        os.makedirs(PHOTO_SAVE_PATH)
    MDEDITOR_FILE_UPLOADER = PHOTO_SAVE_PATH
    # 青牛云存储的设置
    QINIU_ACCESS_KEY = os.getenv('ACCESS_KEY', "KSH6HWWJCKZHYyPyRRITljLkqEt3cJ0QYdUPMoar")
    QINIU_SECRET_KEY = os.getenv('QINIU_KEY', "-X0yBa3CVu6s39i2KzqAV4jBj-a7clmttyCqNJAf")
    QINIU_BUCKET_NAME = 'hyf-test'  # 青牛云存储空间名称
    QINIU_BUCKET_DOMAIN = 'huyinfu.shop'  # 青牛云空间绑定的域名
    # 文章的分页数
    BLUELOG_POST_PER_PAGE = 3
    # 文章评论的分页数
    BLUELOG_COMMENT_PER_PAGE = 3
    # 分类的分页数
    BLUELOG_CATEGORY_PER_PAGE = 3
    # 富文本编辑器设置CKEditor
    CKEDITOR_ENABLE_CSRF = True
    CKEDITOR_FILE_UPLOADER = 'user.upload'
    BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['ico', 'png', 'jpg', 'jpeg', 'gif']
    # 搜索结果的分页数
    BLUELOG_SEARCH_RESULT_PER_PAGE = 10
    # 用户展示分页数
    BLUELOG_USER_PER_PAGE = 3
    # 用户通知的分页数
    BLUELOG_NOTIFICATION_PER_PAGE = 3
    # 创建rsa的公钥保存文件夹
    if not os.path.exists(RAS_PATH):
        os.makedirs(RAS_PATH)


# 俩种配置
class DevelopmentConfig(BaseConfig):
    ENV = 'development'
    DEBUG = True


class ProductionConfig(BaseConfig):
    ENV = 'production'
    DEBUG = False
