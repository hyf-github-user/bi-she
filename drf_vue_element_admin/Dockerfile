FROM huyinfudocker/blog-python:v1
COPY . /home/blog/blog_backed_django
WORKDIR /home/blog/blog_backed_django
RUN pip install uwsgi -i https://mirrors.aliyun.com/pypi/simple/
CMD [ "bash" "-c" "python3 manage.py makemigrations oauth monitor information && python3 manage.py migrate" ] 
