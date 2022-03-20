# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2021/12/31 11:52
from flask import Blueprint, render_template, send_from_directory, current_app, request, flash, url_for, redirect, abort
from flask_login import current_user, login_required
from exts import db
from myapp.blueprints.main.forms import CommentForm
from myapp.decorators import permission_required, confirm_required
from myapp.models.user import Post, Category, Comment, User, Collect, Notification
from myapp.utils import redirect_back
from myapp.utils.notifications import push_comment_notification, push_collect_notification

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    蓝客的主页面
    :return:
    """
    if current_user.is_authenticated:
        page = request.args.get('page', 1, type=int)
        per_page = current_app.config['BLUELOG_POST_PER_PAGE']
        # 获取与当前用户相关的文章
        pagination = Post.query \
            .order_by(Post.timestamp.desc()) \
            .paginate(page, per_page)
        posts = pagination.items
    else:
        posts = None
        pagination = None

    return render_template('main/index.html', posts=posts, pagination=pagination)


@main_bp.route('/explore')
def explore():
    """
    社区中心
    :return:
    """
    return render_template('main/explore.html')


@main_bp.route('/avatars/<path:filename>')
def get_avatar(filename):
    """
    获取头像图片
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config['AVATARS_SAVE_PATH'], filename=filename)


@main_bp.route('/search')
def search():
    q = request.args.get('q', '').strip()
    if q == '':
        flash('输入关于文章或用户或分类的关键字', 'warning')
        return redirect_back()
    category = request.args.get('category', 'post')
    # 获取当前页面
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_SEARCH_RESULT_PER_PAGE']
    if category == 'user':
        pagination = User.query.whooshee_search(q).paginate(page, per_page)
    else:
        pagination = Post.query.whooshee_search(q).paginate(page, per_page)
    results = pagination.items
    return render_template('main/search.html', q=q, results=results, pagination=pagination, category=category)


@main_bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    """
    展示文章详情
    :param post_id:
    :return:
    """
    # 根据id查找文章
    post = Post.query.get_or_404(post_id)
    # 获取当前评论的页数
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_COMMENT_PER_PAGE']
    # 获取评论分页对象(查询被管理员收到的评论)
    pagination = Comment.query.with_parent(post).filter_by(reviewed=True).order_by(Comment.timestamp.asc()).paginate(
        page, per_page)
    comments = pagination.items
    form = CommentForm()
    return render_template('main/post.html', comments=comments, post=post, pagination=pagination,
                           form=form)


@main_bp.route('/report/post/<int:post_id>', methods=['POST'])
def report_post(post_id):
    """
    举报文章
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    post.flag += 1
    db.session.commit()
    flash("文章已举报!", 'success')
    return redirect(url_for('main.show_post', post_id=post_id))


@main_bp.route('/category/<int:category_id>')
def show_category(category_id):
    """
    展示分类详情
    :param category_id:
    :return:
    """
    # 获取分类
    category = Category.query.get_or_404(category_id)
    # 获取分类的分页的页数
    page = request.args.get('page', 1, type=int)
    # 获取分类的每页的数量
    per_page = current_app.config['BLUELOG_CATEGORY_PER_PAGE']
    # 获取分页对象
    pagination = Post.query.with_parent(category).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('main/category.html', category=category, pagination=pagination, posts=posts)


@main_bp.route('/post/<int:post_id>/comment/new', methods=['POST'])
@login_required
@permission_required('COMMENT')
def new_comment(post_id):
    """
    创建文章评论
    :param post_id:
    :return:
    """
    # 根据ID获取评论对象
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    form = CommentForm()
    # 验证评论的表单
    if form.validate_on_submit():
        body = form.body.data
        author = current_user._get_current_object()
        comment = Comment(body=body, post=post, author=author, reviewed=True)
        # 判断是否是回复评论
        replied_id = request.args.get('reply')
        if replied_id:
            comment.replied = Comment.query.get_or_404(replied_id)
            # 判断用户是否收到回复评论的消息通知
            if comment.replied.author.receive_comment_notification:
                push_comment_notification(post_id=post.id, receiver=comment.replied.author)
        db.session.add(comment)
        db.session.commit()
        flash('评论已发表!', 'success')
        # 文章的新评论通知
        if current_user != post.author and post.author.receive_comment_notification:
            push_comment_notification(post_id, receiver=post.author, page=page)
    return redirect(url_for('main.show_post', post_id=post_id, page=page))


@main_bp.route('/reply/comment/<int:comment_id>')
@login_required
@permission_required('COMMENT')
def reply_comment(comment_id):
    """
    回复评论
    :param comment_id:
    :return:
    """
    comment = Comment.query.get_or_404(comment_id)
    return redirect(url_for('main.show_post',
                            post_id=comment.post.id,
                            reply=comment.id,
                            author=comment.author.name) + '#comment-form')


@main_bp.route('/set_comment/<int:post_id>', methods=['POST'])
@login_required
@permission_required('COMMENT')
def set_comment(post_id):
    """
    设置评论功能
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)

    if post.can_comment:
        post.can_comment = False
        flash('评论已禁止!', 'info')
    else:
        post.can_comment = True
        flash('评论已开启!', 'info')
    db.session.commit()
    return redirect(url_for('main.show_post', post_id=post_id))


@main_bp.route('/delete/comment/<int:comment_id>', methods=['POST'])
@login_required
@permission_required('COMMENT')
def delete_comment(comment_id):
    """
    删除评论
    :param comment_id:
    :return:
    """
    comment = Comment.query.get_or_404(comment_id)
    if current_user != comment.author and current_user != comment.post.author \
            and not current_user.can('MODERATE'):
        abort(403)
    db.session.delete(comment)
    db.session.commit()
    flash("评论已删除!", 'success')
    return redirect(url_for('main.show_post', post_id=comment.post_id))


@main_bp.route('/report/comment/<int:comment_id>')
@login_required
def report_comment(comment_id):
    """
    举报评论
    :param comment_id:
    :return:
    """
    comment = Comment.query.get_or_404(comment_id)
    comment.flag += 1
    db.session.commit()
    flash('评论已被举报!', 'success')
    return redirect(url_for('main.show_post', post_id=comment.post_id))


@main_bp.route('/collect/<int:post_id>', methods=['POST'])
@login_required
@confirm_required
@permission_required('COLLECT')  # 判断是否有收藏的权限
def collect(post_id):
    """
    用户收藏文章
    :param post_id:
    :return:
    """
    # 获取需要收藏的文章
    post = Post.query.get_or_404(post_id)
    # 判断用户是否收藏这个文章
    if current_user.is_collecting(post):
        flash("文章已被收藏!", 'info')
        return redirect(url_for('main.show_post', post_id=post.id))
    # 用户收藏文章(也包括匿名用户的收藏)
    current_user.collect(post)
    flash("文章已收藏!", 'success')
    # # 推送文章被收藏的通知
    push_collect_notification(collector=current_user, post_id=post_id, receiver=post.author)
    return redirect_back()


# 取消收藏
@main_bp.route('/uncollect/<int:post_id>', methods=['POST'])
@login_required
@confirm_required
@permission_required('COLLECT')  # 判断是否有收藏的权限
def uncollect(post_id):
    """
    取消收藏文章
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    # 判断是否被收藏
    if not current_user.is_collecting(post):
        flash("文章没有被收藏,不用取消!", 'info')
        return redirect_back()

    current_user.uncollect(post)
    flash("文章已取消收藏!", "success")
    return redirect_back()


# 展示文章的所有关注者
@main_bp.route('/post/<int:post_id>/collectors')
@login_required
@confirm_required
def show_collectors(post_id):
    """
    显示文章的收藏者
    :param post_id:
    :return:
    """
    # 获取显示文章
    post = Post.query.get_or_404(post_id)
    # 获取显示文章的分页数
    page = request.args.get('page', type=int)
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 获取文章收藏的分页对象
    pagination = Collect.query.with_parent(post).order_by(Collect.timestamp.asc()).paginate(page, per_page)
    collects = pagination.items
    return render_template('main/collectors.html', collects=collects, post=post, pagination=pagination)


@main_bp.route('/notifications')
@login_required
def show_notifications():
    """
    展示用户的通知
    :return:
    """
    # 获取页数
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_NOTIFICATION_PER_PAGE']
    notifications = Notification.query.with_parent(current_user)
    # 获取过滤的关键字
    filter_rule = request.args.get('filter')
    if filter_rule == 'unread':
        # 获取未读的通知数
        notifications = notifications.filter_by(is_read=False)

    pagination = notifications.order_by(Notification.timestamp.desc()).paginate(page, per_page)
    notifications = pagination.items
    return render_template('main/notifications.html', pagination=pagination, notifications=notifications)


@main_bp.route('/notification/read/<int:notification_id>', methods=['POST'])
@login_required
def read_notification(notification_id):
    """
    确认单个通知
    :param notification_id:
    :return:
    """
    notification = Notification.query.get_or_404(notification_id)
    if current_user != notification.receiver:
        abort(403)

    notification.is_read = True
    db.session.commit()
    flash('通知已确认!', 'success')
    return redirect(url_for('main.show_notifications'))


@main_bp.route('/notifications/read/all', methods=['POST'])
@login_required
def read_all_notification():
    """
    确认所有通知
    :return:
    """
    for notification in current_user.notifications:
        notification.is_read = True
    db.session.commit()
    flash('所有通知已确认!', 'success')
    return redirect(url_for('main.show_notifications'))
