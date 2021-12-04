# 作者：我只是代码的搬运工
# coding:utf-8


# 遇到错误时返回基类
from flask import request, json
from werkzeug.exceptions import HTTPException


# 遇到错误时返回基类
class APIException(HTTPException):
    # 遇到未知的错误默认返回的code
    code = 500
    msg = '出错啦!'
    error_code = 999

    # 初始化函数
    def __init__(self, code=None, msg=None, error_code=None,
                 headers=None):
        if code:
            self.code = code
        if error_code:
            self.error_code = error_code
        if msg:
            self.msg = msg
        super(APIException, self).__init__(msg, None)  # 实现基类的构造方法

    # 获取请求体信息
    def get_body(self, environ=None):
        body = dict(
            msg=self.msg,
            error_code=self.error_code,
            request=request.method + ' ' + self.get_url_no_param()
        )
        text = json.dumps(body)
        return text

    # 获得请求头的信息
    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [('Content-Type', 'application/json')]

    # 获取没有参数的URL
    @staticmethod
    def get_url_no_param():
        full_path = str(request.full_path)
        main_path = full_path.split('?')
        return main_path[0]
