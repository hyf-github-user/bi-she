# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2022/1/30 23:47
from flask import Blueprint

ajax_bp = Blueprint("ajax", __name__)


@ajax_bp.route('/get_profile')
def get_profile():
    pass
