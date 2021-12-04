# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint

from myapp.utils.network import Result

api_article = Blueprint("api_article", __name__)


# 获取文章列表
@api_article.route('/article/list/<int:page>/<int:limit>')
def get_article(page, limit):
    print(page, limit)
    return Result.error(data="收到请求!")
