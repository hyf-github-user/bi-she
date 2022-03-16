# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :middleware.py
# 时间    :2022/3/14 14:34
from django.utils.deprecation import MiddlewareMixin
from rest_framework.response import Response


class ResponseMiddleware(MiddlewareMixin):
    """
    自定义响应数据格式,使用中间件
    """

    def process_request(self, request):
        pass

    def process_view(self, request, view_func, view_args, view_kwargs):
        pass

    def process_exception(self, request, exception):
        pass

    def process_response(self, request, response):
        if isinstance(response, Response) and response.get('content-type') == 'application/json':
            if response.status_code >= 400:
                msg = '请求失败'
                detail = response.data.get('detail')
                code = 1
                data = {}
            elif response.status_code == 200 or response.status_code == 201:
                msg = '成功'
                detail = ''
                code = 200
                data = response.data
            else:
                return response
            response.data = {'msg': msg, 'errors': detail, 'code': code, 'data': data}
            response.content = response.rendered_content
        return response
