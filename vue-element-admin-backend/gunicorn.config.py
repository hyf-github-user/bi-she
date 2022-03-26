# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :gunicorn.config.py
# 时间    :2022/3/23 11:13
workers = 5 # 定义同时开启的处理请求的进程数量，根据网站流量适当调整

worker_class = "gevent" # 采用gevent库，支持异步处理请求，提高吞吐量

bind = "0.0.0.0:8080" # 这里8080可以随便调整
