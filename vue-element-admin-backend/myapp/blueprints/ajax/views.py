# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2022/1/30 23:47
from flask import Blueprint, jsonify, render_template
from flask_login import current_user

from myapp.models.user import Post, User

ajax_bp = Blueprint("ajax", __name__)


@ajax_bp.route('/profile/<int:user_id>')
def get_profile(user_id):
    """
    获取用户个人信息
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    return render_template('main/profile_popup.html', user=user)


@ajax_bp.route('/followers-count/<int:user_id>')
def followers_count(user_id):
    """
    获取用户的粉丝人数
    :param user_id:
    :return:
    """
    user = User.query.get_or_404(user_id)
    count = user.followers.count() - 1  # 获取粉丝数(除去自己)
    return jsonify(count=count)


@ajax_bp.route('/<int:post_id>/followers-count')
def collectors_count(post_id):
    """
    获取文章的总收藏数
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    count = len(post.collectors)
    return jsonify(count=count)


@ajax_bp.route('/collect/<int:post_id>', methods=['POST'])
def collect(post_id):
    """
    用户收藏文章
    :param post_id:
    :return:
    """
    if not current_user.is_authenticated:
        return jsonify(message='需要登录!'), 403
    if not current_user.confirmed:
        return jsonify(message='需要确认用户登录!'), 400
    if not current_user.can('COLLECT'):
        return jsonify(message='没有收藏的权限'), 403

    post = Post.query.get_or_404(post_id)
    if current_user.is_collecting(post):
        return jsonify(message='已经被收藏了!'), 400

    current_user.collect(post)
    # 发送收藏通知
    # if current_user != post.author and post.author.receive_collect_notification:
    #     push_collect_notification(collector=current_user, post_id=post_id, receiver=post.author)
    return jsonify(message='文章已收藏!')


@ajax_bp.route('/uncollect/<int:post_id>', methods=['POST'])
def uncollect(post_id):
    """
    用户取消收藏文章
    :param post_id:
    :return:
    """
    if not current_user.is_authenticated:
        return jsonify(message='需要登录!'), 403

    post = Post.query.get_or_404(post_id)
    if not current_user.is_collecting(post):
        return jsonify(message='没有收藏!'), 400

    current_user.uncollect(post)
    return jsonify(message='取消收藏成功!')


@ajax_bp.route('/follow/<username>', methods=['POST'])
def follow(username):
    """
    用户关注
    :param username:
    :return:
    """
    if not current_user.is_authenticated:
        return jsonify(message='需要登录!'), 403
    if not current_user.confirmed:
        return jsonify(message='需要确认用户登录!'), 400
    if not current_user.can('FOLLOW'):
        return jsonify(message='没有关注权限'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if current_user.is_following(user):
        return jsonify(message='已经关注了!'), 400

    current_user.follow(user)
    # 发送关注的通知
    # if user.receive_collect_notification:
    #     push_follow_notification(follower=current_user, receiver=user)
    return jsonify(message='关注用户成功!')


@ajax_bp.route('/unfollow/<username>', methods=['POST'])
def unfollow(username):
    """
    取消用户关注
    :param username:
    :return:
    """
    if not current_user.is_authenticated:
        return jsonify(message='需要登录!'), 403

    user = User.query.filter_by(username=username).first_or_404()
    if not current_user.is_following(user):
        return jsonify(message='没有关注!'), 400

    current_user.unfollow(user)
    return jsonify(message='取消关注成功!')
