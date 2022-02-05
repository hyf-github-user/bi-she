# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2022/1/30 23:47
from flask import Blueprint

ajax_bp = Blueprint("ajax", __name__)


@ajax_bp.route('/get_profile/<int:user_id>/')
def get_profile(user_id):
    pass


@ajax_bp.route('/collectors_count/<int:post_id>/')
def collectors_count(post_id):
    pass


@ajax_bp.route('/uncollect/<int:post_id>/', methods=['POST'])
def uncollect(post_id):
    pass


@ajax_bp.route('/collect/<int:post_id>/', methods=['POST'])
def collect(post_id):
    pass
