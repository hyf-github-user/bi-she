# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :views.py
# 时间    :2021/12/31 11:52
from flask import Blueprint, render_template, send_from_directory, current_app, request, flash, url_for, redirect, abort
from flask_login import current_user, login_required
from exts import db
from myapp.blueprints.user.forms import CommentForm
from myapp.decorators import permission_required
from myapp.models.user import Post, Category, Comment, User
from myapp.utils import redirect_back

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
    post = Post.query.get_or_404(post_id)
    page = request.args.get('page', 1, type=int)
    form = CommentForm()
    if form.validate_on_submit():
        body = form.body.data
        author = current_user._get_current_object()
        comment = Comment(body=body, post=post, author=author, reviewed=True)
        replied_id = request.args.get('reply')
        if replied_id:
            comment.replied = Comment.query.get_or_404(replied_id)
            # if comment.replied.author.receive_comment_notification:
            #     push_comment_notification(photo_id=photo.id, receiver=comment.replied.author)
        db.session.add(comment)
        db.session.commit()
        flash('评论已发表!', 'success')

        # if current_user != post.author and post.author.receive_comment_notification:
        #     push_comment_notification(photo_id, receiver=post.author, page=page)
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
    return redirect(url_for('main.show_post', photo_id=comment.post_id))
