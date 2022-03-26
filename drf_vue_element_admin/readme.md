## drf框架实现步骤
### 安装依赖
```shell
pip install -r requirements.txt
```
### 数据库密码更改
```python
# mysql密码配置
DATABASES = {
    # 配置mysql数据库
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'grad_pro',  # 数据库库名（需提前创建好数据库）
        'USER': 'root',  # 用户名
        'PASSWORD': '*****',  # 连接密码
        'HOST': '127.0.0.1',  # 主机
        'PORT': '3306',  # mysql端口
    }
}
# Redis
REDIS_PWD = os.getenv('REDIS_PWD', '******')
```
### 运行过程
```shell
# 迁移生成数据库模型
python manage.py makemigrations oauth monitor information
# 数据库模型迁移同步到数据库
python manage.py migrate
# 创建超级用户用于管理系统登录
python manage.py createsuperuser 
# 运行后端接口服务,必须是在8000端口
python manage.py runserver 127.0.0.1:8000
```
