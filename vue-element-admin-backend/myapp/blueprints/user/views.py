# 作者：我只是代码的搬运工
# coding:utf-8
import os
from datetime import datetime
from flask import Blueprint, request, render_template, url_for, jsonify, current_app, send_from_directory, \
    flash, redirect
from flask_login import current_user, login_required, logout_user
from exts import csrf, db
from myapp.models.user import Post, Category, User

user_bp = Blueprint("user", __name__)


@user_bp.route('/<username>')
def index(username):
    """
    个人主页
    :param username:
    :return:
    """
    user = User.query.filter_by(username=username).first_or_404()  # 查询用户
    if user.locked and user == current_user:
        flash("当前用户已锁定!", 'danger')
    if user == current_user and not user.active:
        # 未被激活,退出登录
        logout_user()
    page = request.args.get('page', 1, type=int)  # 获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']  # 文章分页数
    # 获取分页对象
    pagination = Post.query.with_parent(user).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('user/index.html', posts=posts, user=user, pagination=pagination)


@user_bp.route('/post/upload', methods=['POST'])
@csrf.exempt
def upload():
    """
    上传文件,并进行保存
    :return:
    """
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(current_app.config['PHOTO_SAVE_PATH'], filename))
        res = {
            'success': 1,
            'message': '上传成功',
            'url': url_for('.image', filename=filename)
        }
    return jsonify(res)


@user_bp.route('/post/image/<filename>')
def image(filename):
    """
    展示文章的图片
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config['PHOTO_SAVE_PATH'], filename=filename)


@user_bp.route('/post/new', methods=['GET', 'POST'])
@csrf.exempt  # 忽略csrf保护
@login_required  # 确保管理员已登录
def new_post():
    """
    创建文章并发布
    :return:
    """
    if request.method == 'GET':
        return render_template('editormd_post/new_post.html')
    else:
        title = request.form['title']
        body = request.form['content']
        body_html = request.form['fancy-editormd-html-code']
        category = Category.query.filter_by(name=request.form['category']).first_or_404()
        post = Post(title=title, body=body, body_html=body_html, category=category,
                    author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash("文章已发表!", 'success')
        return redirect(url_for('main.show_post', post_id=post.id))


@user_bp.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """
    更新文章
    :param post_id:
    :return:
    """
    # 获取当前的文章
    post = Post.query.get_or_404(post_id)
    if request.method == 'GET':
        return render_template('editormd_post/edit_post.html', post=post)
    else:
        post.title = request.form['title']
        post.body = request.form['content']
        post.body_html = request.form['fancy-editormd-html-code']
        post.category = Category.query.filter_by(name=request.form['category']).first_or_404()
        db.session.commit()
        flash("文章已更新!!", 'success')
        return redirect(url_for('main.show_post', post_id=post.id))


@user_bp.route('/post/<int:post_id>/delete')
@login_required
def delete_post(post_id):
    """
    删除文章
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.show_post', post_id=post.id))
