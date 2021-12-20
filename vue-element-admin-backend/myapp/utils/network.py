# 作者：我只是代码的搬运工
# coding:utf-8
import json
from datetime import datetime

from flask import Response


# 重写时间的转换方法
class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self, obj)


class Result:
    """
    请求响应的返回
    """

    # 成功默认返回200,data是success
    @staticmethod
    def success(**kwargs):
        data = {
            "code": 200,
            "data": 'success',
            "jwt": ''
        }
        data.update(kwargs)
        return Response(json.dumps(data, cls=DateEncoder))

    # 错误默认返回400错误
    @staticmethod
    def error(**kwargs):
        data = {
            "code": 400,
            "message": "error"
        }
        data.update(kwargs)
        return Response(json.dumps(data, cls=DateEncoder))
