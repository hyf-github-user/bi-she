FROM huyinfudocker/blog-python:v1
COPY . /home/blog/blog_front
WORKDIR /home/blog/blog_front
RUN rm -rf migrations
RUN pip install uwsgi -i https://mirrors.aliyun.com/pypi/simple/
CMD [ "bash" "-c" "python3 app.py db init && python3 app.py db migrate -m "数据库完成" && python3 app.py db upgrade"]