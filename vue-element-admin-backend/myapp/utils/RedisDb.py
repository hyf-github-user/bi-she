# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :RedisDb.py
# 时间    :2022/1/22 17:33
import redis


class RedisDb:

    def __init__(self, REDIS_HOST='127.0.0.1', REDIS_PORT='6379', REDIS_PASSWORD='hu15879093053', EXPIRE_TIME=600,
                 REDIS_DB=4):
        # 建立Redis连接
        self.redis = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD, db=REDIS_DB,
                                 decode_responses=True)
        self.expire_time = EXPIRE_TIME

    def handle_captcha(self, code, captcha=None):
        code = '验证码:' + code
        # 判断是否有验证码
        if captcha:
            # 存入Redis
            self.redis.set(code, captcha, ex=self.expire_time)
        else:
            captcha = self.redis.get(code)
            return captcha

    def handle_token(self, user, token):
        # 判断是否有token
        if token:
            # 存入Redis
            self.redis.set(user, token, ex=self.expire_time)
        else:
            token = self.redis.get(user)
            return token
