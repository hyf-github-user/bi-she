# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2021/12/31 11:52
from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    主页面
    :return:
    """
    return render_template('main/index.html')


@main_bp.route('/explore')
def explore():
    """

    :return:
    """
    return render_template('main/explore.html')
