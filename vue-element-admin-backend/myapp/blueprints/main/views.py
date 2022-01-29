# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2021/12/31 11:52
from flask import Blueprint, render_template, send_from_directory, current_app, request
from flask_login import current_user

from myapp.models.user import Post

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    主页面
    :return:
    """
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['BLUELOG_POST_PER_PAGE']
        pagination = Post.query \
            .order_by(Post.timestamp.desc()) \
            .paginate(page, per_page)
        posts = pagination.items
    else:
        pagination = None
        photos = None

    return render_template('main/index.html', posts=posts)


@main_bp.route('/explore')
def explore():
    """

    :return:
    """
    return render_template('main/explore.html')


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename=filename)
