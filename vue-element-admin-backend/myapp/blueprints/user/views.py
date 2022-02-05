# 作者：我只是代码的搬运工
# coding:utf-8
import os
from datetime import datetime
from flask import Blueprint, request, render_template, url_for, jsonify, current_app, send_from_directory, \
    flash, redirect
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required, logout_user
from exts import csrf, db
from myapp.blueprints.user.forms import PostForm, CategoryForm, LinkForm
from myapp.models.user import Post, Category, User, Link
from myapp.utils import allowed_file

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
    file = request.files.get('upload')
    if not allowed_file(file.filename):
        return upload_fail('必须是照片!')
    ex = os.path.splitext(file.filename)[1]
    filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
    file.save(os.path.join(current_app.config['PHOTO_SAVE_PATH'], filename))
    url = url_for('user.image', filename=filename)
    return upload_success(url, filename)


@user_bp.route('/post/image/<filename>')
def image(filename):
    """
    展示文章的图片
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config['PHOTO_SAVE_PATH'], filename=filename, as_attachment=True)


@user_bp.route('/post/new', methods=['GET', 'POST'])
@csrf.exempt  # 忽略csrf保护
@login_required  # 确保管理员已登录
def new_post():
    """
    创建文章并发布
    :return:
    """
    # 创建文章表单
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        category = Category.query.get(form.category.data)
        post = Post(title=title, body=body, category=category, author=current_user._get_current_object())
        # 开始提交到数据库
        db.session.add(post)
        db.session.commit()
        # flash提示信息
        flash("文章已创建!", 'success')
        return redirect(url_for('main.show_post', post_id=post.id))
    return render_template('user/new_post.html', form=form)


@user_bp.route('/post/manage')
@login_required
def manage_post():
    # page = request.args.get('page', 1, type=int)
    # pagination = Post.query.order_by(Post.timestamp.desc()).paginate(page, per_page=current_app.config[
    #     'BLUELOG_MANAGE_POST_PER_PAGE'])
    # posts = pagination.items

    return render_template('user/manage_post.html')


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
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.body = form.body.data
        post.category = Category.query.get(form.category.data)
        db.session.commit()
        flash("文章更新成功!", 'success')
        return redirect(url_for('main/show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('user/edit_post.html', post=post)


@user_bp.route('/post/<int:post_id>/delete', methods=['POST'])
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


@user_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash("分类已创建!", 'success')
        return redirect(url_for('user.manage_category'))
    return render_template('user/new_category.html', form=form)


@user_bp.route('/category/manage')
@login_required
def manage_category():
    """
    管理分类
    :return:
    """
    return render_template('user/manage_category.html')


@user_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    form = CategoryForm()
    category = Category.query.get_or_404(category_id)
    if form.validate_on_submit():
        category.name = form.name.data
        db.session.commit()
        flash("分类已更新!", 'info')
        return redirect(url_for('user.manage_category'))

    return render_template('user/edit_category.html', form=form)


@user_bp.route('/category/<int:category_id>/delete')
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    flash("分类已删除!", 'info')
    return redirect(url_for('user.manage_category'))


@user_bp.route('/link/new', methods=['GET', 'POST'])
@login_required
def new_link():
    form = LinkForm()
    if form.validate_on_submit():
        name = form.name.data
        url = form.url.data
        link = Link(name=name, url=url)
        db.session.add(link)
        db.session.commit()
        flash("链接已添加!", 'success')
        return redirect(url_for('user.manage_link'))

    return render_template('user/new_link.html', form=form)


@user_bp.route('/link/manage')
@login_required
def manage_link():
    """
    管理链接
    :return:
    """
    return render_template('user/manage_link.html')


@user_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_link(link_id):
    """
    编辑链接
    :param link_id:
    :return:
    """
    link = Link.query.get_or_404(link_id)
    form = LinkForm()
    if form.validate_on_submit():
        link.name = form.name.data
        link.url = form.url.data
        db.session.commit()
        flash("链接更新成功!", 'success')
        return redirect(url_for('user.manage_link'))

    form.name.data = link.name
    form.url.data = link.url

    return render_template('user/edit_link.html', form=form)


@user_bp.route('link/<int:link_id>/delete', methods=['POST'])
@login_required
def delete_link(link_id):
    """
    删除链接
    :param link_id:
    :return:
    """
    link = Link.query.get_or_404(link_id)
    db.session.delete(link)
    db.session.commit()
    flash("链接已删除!", 'info')
    return redirect(url_for('user.manage_link'))
