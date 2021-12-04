# 作者：我只是代码的搬运工
# coding:utf-8

from flask import make_response, jsonify

SUCCESS = {
    "code": 20000,
    "data": "success"
}

NOTFOUND = {
    "code": 20000,
    "data": "not found"
}

AUTHFAILED = {
    "code": 20000,
    "data": "auth failed"
}

EXPIRED = {
    "code": 50012,
    "data": "token is expired"
}

FORBIDDEN = {
    "code": 20000,
    "data": "forbidden, not in scope"
}


# 返回一种json形式的状态码
def response_data(response):
    return make_response(jsonify(response))

# class Result:
#     """
#     响应返回
#     """
#
#     @staticmethod
#     def success(**kwargs):
#         payload = {
#             'code': 200,
#             'message': 'ok'
#         }
#         payload.update(kwargs)
#         return Response(payload, status=200)
#
#     @staticmethod
#     def error(**kwargs):
#         payload = {
#             'code': status.HTTP_500_INTERNAL_SERVER_ERROR,
#             'message': 'error'
#         }
#         payload.update(kwargs)
#         return Response(data=payload, status=200 if 'code' not in kwargs.keys() else kwargs['code'])
