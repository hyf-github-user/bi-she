# 安装依赖
pip install -r requirements.txt
# 更换密码
```python
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:hu15879093053@localhost:3306/grad_pro'
```
# 数据库进行迁移同步
```shell
python app.py db init
python app.py db migrate -m "数据库设计完成"
python app.py db upgrade
```
# 运行后端
```shell
python app.py runserver
```
