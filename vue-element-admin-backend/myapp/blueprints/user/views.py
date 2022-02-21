# 作者：我只是代码的搬运工
# coding:utf-8
import os
from datetime import datetime
from flask import Blueprint, request, render_template, url_for, current_app, send_from_directory, \
    flash, redirect, abort
from flask_ckeditor import upload_fail, upload_success
from flask_login import current_user, login_required, logout_user, fresh_login_required
from exts import db, qiniu_store, avatars
from myapp.blueprints.user.forms import PostForm, CategoryForm, LinkForm, EditProfileForm, ChangePasswordForm, \
    ChangeEmailForm, NotificationSettingForm, PrivacySettingForm, DeleteAccountForm, UploadAvatarForm, CropAvatarForm
from myapp.decorators import confirm_required, permission_required
from myapp.models.user import Post, Category, User, Link, Collect
from myapp.utils import allowed_file, redirect_back
from myapp.utils.emails import send_change_email_email
from myapp.utils.token import generate_token, validate_token
from settings import Operations

user_bp = Blueprint("user", __name__)


@user_bp.route('/<username>')
@login_required
def index(username):
    """
    个人主页
    :param username:
    :return:
    """
    # 根据用户ID查询用户
    user = User.query.filter_by(username=username).first_or_404()  # 查询用户
    # 判断用户是否被锁定
    if user.locked:
        flash("当前用户已锁定!", 'danger')
    # 判断用户是否被激活
    if user == current_user and not user.active:
        # 未被激活,退出登录
        logout_user()
    # 获取当前的文章的页数
    page = request.args.get('page', 1, type=int)  # 获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']  # 文章分页数
    # 获取分页对象(获取当前用户的文章)
    pagination = Post.query.with_parent(user).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('user/index.html', posts=posts, user=user, pagination=pagination)


@user_bp.route('/post/upload', methods=['POST'])
@login_required
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
    # 保存到青牛云里面
    qiniu_store.save(file, filename)
    # 获取青牛云存储的URL
    url = qiniu_store.url(filename)
    # 保存到本地的图片
    # file.save(os.path.join(current_app.config['PHOTO_SAVE_PATH'], filename))
    # url = url_for('user.image', filename=filename)
    return upload_success(url, filename)


@user_bp.route('/post/image/<filename>')
def image(filename):
    """
    展示文章的图片(保存在本地的图片),不保存到本地可弃用
    :param filename:
    :return:
    """
    return send_from_directory(current_app.config['PHOTO_SAVE_PATH'], filename=filename, as_attachment=True)


@user_bp.route('/post/new', methods=['GET', 'POST'])
@login_required  # 确保管理员已登录
@confirm_required  # 验证确认状态
def new_post():
    """
    创建文章并发布
    :return:
    """
    # 创建文章表单
    form = PostForm()
    if form.validate_on_submit():
        # 获取文章表单数据
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


@user_bp.route('/post/manage/<username>')
@login_required
def manage_post(username):
    """
    管理当前用户发表的文章
    :param username:
    :return:
    """
    # 根据用户ID查询用户
    user = User.query.filter_by(username=username).first_or_404()  # 查询用户
    # 判断用户是否被锁定
    if user.locked:
        flash("当前用户已锁定!", 'danger')
    # 判断用户是否被激活
    if user == current_user and not user.active:
        # 未被激活,退出登录
        logout_user()
    # 获取当前的文章的页数
    page = request.args.get('page', 1, type=int)  # 获取当前页数
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']  # 文章分页数
    # 获取分页对象(获取当前用户的文章)
    pagination = Post.query.with_parent(user).order_by(Post.timestamp.desc()).paginate(page, per_page)
    posts = pagination.items
    return render_template('user/manage_post.html', posts=posts, pagination=pagination, user=user)


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
        return redirect(url_for('main.show_post', post_id=post.id))
    form.title.data = post.title
    form.body.data = post.body
    form.category.data = post.category_id
    return render_template('user/edit_post.html', form=form)


@user_bp.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """
    删除文章
    :param post_id:
    :return:
    """
    post = Post.query.get_or_404(post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user.manage_post', username=post.author.username))


@user_bp.route('/category/new', methods=['GET', 'POST'])
@login_required
def new_category():
    """
    创建新的分类
    :return:
    """
    # 创建分类表单
    form = CategoryForm()
    if form.validate_on_submit():
        name = form.name.data
        category = Category(name=name)
        db.session.add(category)
        db.session.commit()
        flash("分类已创建!", 'success')
        return redirect_back()
    return render_template('user/new_category.html', form=form)


# 分类的管理接口
# @user_bp.route('/category/manage/<username>')
# @login_required
# def manage_category(username):
#     """
#     管理分类
#     :return:
#     """
#     # 根据用户ID查询用户
#     user = User.query.filter_by(username=username).first_or_404()  # 查询用户
#     # 判断用户是否被锁定
#     if user.locked:
#         flash("当前用户已锁定!", 'danger')
#     # 判断用户是否被激活
#     if user == current_user and not user.active:
#         # 未被激活,退出登录
#         logout_user()
#     # 获取当前的文章的页数
#     page = request.args.get('page', 1, type=int)  # 获取当前页数
#     per_page = current_app.config['BLUELOG_POST_PER_PAGE']  # 文章分页数
#     # 获取分页对象(获取当前用户的文章)
#     pagination = Post.query.with_parent(user).order_by(Post.timestamp.desc()).paginate(page, per_page)
#     posts = pagination.items
#     return render_template('user/manage_category.html')
#
#
# @user_bp.route('/category/<int:category_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_category(category_id):
#     form = CategoryForm()
#     category = Category.query.get_or_404(category_id)
#     if form.validate_on_submit():
#         category.name = form.name.data
#         db.session.commit()
#         flash("分类已更新!", 'info')
#         return redirect(url_for('user.manage_category'))
#
#     return render_template('user/edit_category.html', form=form)
#
#
# @user_bp.route('/category/<int:category_id>/delete')
# @login_required
# def delete_category(category_id):
#     category = Category.query.get_or_404(category_id)
#     db.session.delete(category)
#     db.session.commit()
#     flash("分类已删除!", 'info')
#     return redirect(url_for('user.manage_category',))


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
        return redirect_back()

    return render_template('user/new_link.html', form=form)


# 友情链接的管理接口
# @user_bp.route('/link/manage')
# @login_required
# def manage_link():
#     """
#     管理链接
#     :return:
#     """
#     return render_template('user/manage_link.html')
#
#
# @user_bp.route('/link/<int:link_id>/edit', methods=['GET', 'POST'])
# @login_required
# def edit_link(link_id):
#     """
#     编辑链接
#     :param link_id:
#     :return:
#     """
#     link = Link.query.get_or_404(link_id)
#     form = LinkForm()
#     if form.validate_on_submit():
#         link.name = form.name.data
#         link.url = form.url.data
#         db.session.commit()
#         flash("链接更新成功!", 'success')
#         return redirect(url_for('user.manage_link'))
#
#     form.name.data = link.name
#     form.url.data = link.url
#
#     return render_template('user/edit_link.html', form=form)
#
#
# @user_bp.route('link/<int:link_id>/delete', methods=['POST'])
# @login_required
# def delete_link(link_id):
#     """
#     删除链接
#     :param link_id:
#     :return:
#     """
#     link = Link.query.get_or_404(link_id)
#     db.session.delete(link)
#     db.session.commit()
#     flash("链接已删除!", 'info')
#     return redirect(url_for('user.manage_link'))


@user_bp.route('/follow/<username>', methods=['POST'])
@login_required
@confirm_required
@permission_required('FOLLOW')
def follow(username):
    """
    关注用户视图
    :param username:
    :return:
    """
    # 获取要关注的用户
    user = User.query.filter_by(username=username).first_or_404()
    # 判断用户是否关注了他
    if current_user.is_following(user):
        flash("已经关注了!", 'info')
        return redirect(url_for('user.index', username=username))
    # 用户关注他
    current_user.follow(user)
    flash("此用户已被关注!", 'success')
    # if user.receive_follow_notification:
    #     # 推送消息
    #     push_follow_notification(follower=current_user, receiver=user)
    return redirect_back()


@user_bp.route('unfollow/<username>')
@login_required
def unfollow(username):
    """
     用户取消关注用户
    :param username:
    :return:
    """
    # 获取要取消关注的用户
    user = User.query.filter_by(username=username).first_or_404()
    # 查看用户是否已经关注了他
    if not current_user.is_following(user):
        flash("此用户没被关注,不能取消!", 'info')
        return redirect(url_for('user.index', username=username))
    # 用户取消关注他
    current_user.unfollow(user)
    flash("取消关注成功!", 'success')
    return redirect_back()


# 我关注的人
@user_bp.route('/<username>/following')
def show_following(username):
    """
    显示我关注的人的视图函数
    :param username:
    :return:
    """
    # 通过用户名查询用户
    user = User.query.filter_by(username=username).first_or_404()
    # 获取用户分页
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_USER_PER_PAGE']
    pagination = user.following.paginate(page=page, per_page=per_page)
    follows = pagination.items
    return render_template('user/following.html', user=user, pagination=pagination, follows=follows)


# 查看粉丝数
@user_bp.route('/<username>/followers')
def show_followers(username):
    """
    显示我的粉丝量的视图函数
    :param username:
    :return:
    """
    # 获取要查看粉丝的用户
    user = User.query.filter_by(username=username).first_or_404()
    # 获取用户分页数
    page = request.args.get('page', 1, type=int)
    per_page = current_app.config['BLUELOG_USER_PER_PAGE']
    # 获取粉丝的分页对象
    pagination = user.followers.paginate(page=page, per_page=per_page)
    follows = pagination.items
    return render_template('user/followers.html', user=user, pagination=pagination, follows=follows)


# 展示用户的所有收藏文章
@user_bp.route('/<username>/collectors')
def show_collections(username):
    """
    显示我所有收藏的文章数
    :param username:
    :return:
    """
    # 获取收藏的用户
    user = User.query.filter_by(username=username).first_or_404()
    # 获取当前页数
    page = request.args.get('page', type=int)
    # 获取文章的分页
    per_page = current_app.config['BLUELOG_POST_PER_PAGE']
    # 获取当前用户的所有收藏文章
    pagination = Collect.query.with_parent(user).order_by(Collect.timestamp.desc()).paginate(page, per_page)
    collects = pagination.items
    return render_template('user/collections.html', user=user, pagination=pagination, collects=collects)


@user_bp.route('/settings/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """
    编辑个人信息
    :return:
    """
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.username = form.username.data
        current_user.website = form.website.data
        db.session.commit()
        flash('个人信息已更新!', 'success')
        return redirect(url_for('user.index', username=current_user.username))
    form.name.data = current_user.name
    form.username.data = current_user.username
    form.website.data = current_user.website
    return render_template('user/settings/edit_profile.html', form=form)


@user_bp.route('/settings/change-password', methods=['GET', 'POST'])
@fresh_login_required  # 重新登录
def change_password():
    """
    重置密码
    :return:
    """
    # 生成重置密码的表单
    form = ChangePasswordForm()
    # 验证表单的输入
    if form.validate_on_submit():
        # 验证旧密码
        if current_user.validate_password(form.old_password.data):
            # 设置密码
            current_user.set_password(form.password.data)
            db.session.commit()
            flash('密码已更新!', 'success')
            return redirect(url_for('user.index', username=current_user.username))
        else:
            flash('旧密码错误!', 'warning')
    return render_template('user/settings/change_password.html', form=form)


@user_bp.route('/settings/change-email', methods=['GET', 'POST'])
@fresh_login_required  # 需要重新登录
def change_email_request():
    """
    修改登录邮箱的请求
    :return:
    """
    # 生成修改邮箱的表单
    form = ChangeEmailForm()
    if form.validate_on_submit():
        # 产生验证的token
        token = generate_token(user=current_user, operation=Operations.CHANGE_EMAIL, new_email=form.email.data.lower())
        send_change_email_email(to=form.email.data, user=current_user, token=token)
        flash('确认邮件已发送! 请检查你的邮箱', 'info')
        return redirect(url_for('user.index', username=current_user.username))
    return render_template('user/settings/change_email.html', form=form)


@user_bp.route('/change-email/<token>')
@login_required
def change_email(token):
    """
    验证token并判断是什么操作然后进行相应的操作
    :param token:
    :return:
    """
    # 验证token并进行修改邮箱操作
    if validate_token(user=current_user, token=token, operation=Operations.CHANGE_EMAIL):
        flash('邮箱地址已修改!', 'success')
        return redirect(url_for('user.index', username=current_user.username))
    else:
        flash('token验证失败!', 'warning')
        return redirect(url_for('user.change_email_request'))


@user_bp.route('/settings/notification-setting', methods=['GET', 'POST'])
@login_required
def notification_setting():
    # 通知设置表单
    form = NotificationSettingForm()
    if form.validate_on_submit():
        current_user.receive_collect_notification = form.receive_collect_notification.data
        current_user.receive_comment_notification = form.receive_comment_notification.data
        current_user.receive_follow_notification = form.receive_follow_notification.data
        db.session.commit()
        flash('消息通知设置已更新!', 'success')
        return redirect(url_for('user.index', username=current_user.username))
    form.receive_collect_notification.data = current_user.receive_collect_notification
    form.receive_comment_notification.data = current_user.receive_comment_notification
    form.receive_follow_notification.data = current_user.receive_follow_notification
    return render_template('user/settings/edit_notification.html', form=form)


@user_bp.route('/settings/privacy-setting', methods=['GET', 'POST'])
@login_required
def privacy_setting():
    # 隐私设置表单
    form = PrivacySettingForm()
    if form.validate_on_submit():
        current_user.public_collections = form.public_collections.data
        db.session.commit()
        flash('个人隐私设置已更新!', 'success')
        return redirect(url_for('user.index', username=current_user.username))
    form.public_collections.data = current_user.public_collections
    return render_template('user/settings/edit_privacy.html', form=form)


@user_bp.route('/settings/delete-account', methods=['GET', 'POST'])
@login_required
def delete_account():
    # 注销用户的表单
    form = DeleteAccountForm()
    if form.validate_on_submit():
        db.session.delete(current_user._get_current_object())
        db.session.commit()
        flash('此用户成功被注销!', 'success')
        return redirect(url_for('main.index'))
    return render_template('user/settings/delete_account.html', form=form)


@user_bp.route('/settings/change-avatar', methods=['GET', 'POST'])
@login_required
@confirm_required
def change_avatar():
    """
    修改头像
    :return:
    """
    # 上传头像的表单
    upload_form = UploadAvatarForm()
    # 获取裁剪的头像的表单
    crop_form = CropAvatarForm()
    return render_template('user/settings/change_avatar.html', upload_form=upload_form, crop_form=crop_form)


@user_bp.route('/settings/avatar/upload', methods=['POST'])
@login_required
@confirm_required
def upload_avatar():
    """
    保存上传后的图片
    :return:
    """
    # 上传图片的表单
    form = UploadAvatarForm()
    if form.validate_on_submit():
        # 保存上传后的头像
        image = form.image.data
        filename = avatars.save_avatar(image)
        current_user.avatar_raw = filename
        db.session.commit()
        flash('图片已上传,请裁剪图片', 'success')
    return redirect(url_for('user.change_avatar'))


@user_bp.route('/settings/avatar/crop', methods=['POST'])
@login_required
@confirm_required
def crop_avatar():
    """
    处理裁剪图片后的结果并保存图片
    :return:
    """
    # 裁剪头像的表单
    form = CropAvatarForm()
    if form.validate_on_submit():
        # 获取裁剪头像的结果
        x = form.x.data
        y = form.y.data
        w = form.w.data
        h = form.h.data
        # 使用flask-avatars裁剪图片并保存到数据库中
        filenames = avatars.crop_avatar(current_user.avatar_raw, x, y, w, h)
        current_user.avatar_s = filenames[0]
        current_user.avatar_m = filenames[1]
        current_user.avatar_l = filenames[2]
        db.session.commit()
        flash('头像已更新!', 'success')
    return redirect(url_for('user.change_avatar'))
