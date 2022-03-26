# 作者：我只是代码的搬运工
# coding:utf-8
from io import BytesIO

from flask import Blueprint, flash, redirect, url_for, render_template, make_response, current_app
from flask_login import current_user, login_required, login_user, logout_user, login_fresh, confirm_login

from exts import db
from myapp.blueprints.auth.forms import LoginForm, RegisterForm, ForgetPasswordForm, ResetPasswordForm
from myapp.models.user import User
from myapp.utils import redirect_back
from myapp.utils.RedisDb import RedisDb
from myapp.utils.captcha import Captcha
from myapp.utils.emails import send_confirm_email, send_reset_password_email
from myapp.utils.token import generate_token, validate_token
from settings import Operations

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    """
    # 用户登录视图函数
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # 登录表单
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower()).first()
        if user and user.check_password(form.password.data):
            if login_user(user, form.remember_me.data):  # 记住我登录选项
                flash('登录成功!', 'info')
                return redirect_back()  # 回到首页
            else:
                flash('你的账号已被封禁!', 'warning')
                return redirect(url_for('main.index'))
        flash('邮箱或密码错误!', 'warning')
    return render_template('auth/login.html', form=form)


# 用户注册视图函数
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    """
    注册用户视图
    :return:
    """
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        # 电子邮箱同意大写
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(username=username, name=name, email=email)
        if email == current_app.config['ADMIN_EMAIL']:
            user = User(
                username=username,
                auth=4,
                name=name,
                email=current_app.config['ADMIN_EMAIL'],
                confirmed=True,
                active=True
            )
        # 设置rsa与hash密码
        user.set_password(password=password)
        # 提交到数据库
        db.session.add(user)
        db.session.commit()
        # 生成token
        token = generate_token(user=user, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)  # 发送邮箱进行注册确认,这里不能确认能不能向用户成功发送邮件
        flash('邮箱验证已发送,请检查你的邮箱!', 'info')
        return redirect(url_for('auth.login'))  # 注册完就去登录
    return render_template('auth/register.html', form=form)


# 通过token确认注册
@auth_bp.route('/confirm/<token>')
@login_required  # 此视图需要用户登录
def confirm(token):
    """
    当用户点击确认邮箱所触发的视图函数
    :param token:
    :return:
    """
    # 判断当前用户是否确认了
    if current_user.confirmed:
        return redirect(url_for('main.index'))

    # 开始验证token
    if validate_token(user=current_user, token=token, operation=Operations.CONFIRM):
        flash("该用户已确认!", 'success')
        return redirect(url_for('main.index'))
    else:
        flash("邮箱确认失败!", 'danger')
        return redirect(url_for('auth.resend_confirm_email'))


# 重写发送验证邮箱
@auth_bp.route('/resend-confirm-email')
@login_required  # 需要登录
def resend_confirm_email():
    # 判断当前用户是否已经确认了
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    # 生成token
    token = generate_token(user=current_user, operation=Operations.CONFIRM)
    send_confirm_email(user=current_user, token=token)  # 发送邮箱进行注册确认,这里不能确认能不能向用户成功发送邮件
    flash('邮箱验证已发送,请检查你的邮箱!', 'info')
    return redirect(url_for('main.index'))  # 注册完就去登录


# 用户刷新重新认证
@auth_bp.route('/re_authenticate', methods=['POST', 'GET'])
@login_required
def re_authenticate():
    """
    刷新登录,防止超时
    :return:
    """
    # 判断当前用户对话是否超时
    if login_fresh():
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit() and current_user.validate_password(form.password.data):
        # 重新登录
        confirm_login()
        return redirect_back()

    return render_template('auth/login.html', form=form)


# 忘记密码视图函数
@auth_bp.route('/forget-password', methods=['POST', 'GET'])
def forget_password():
    # 判断当前用户是否登录
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # 创建忘记密码的表单
    form = ForgetPasswordForm()
    if form.validate_on_submit():
        # 获取表单的email
        email = form.email.data.lower()
        # 根据输入的邮箱查找用户
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_token(user=user, operation=Operations.RESET_PASSWORD)
            send_reset_password_email(user=user, token=token)
            flash('密码重置消息已发送!请查看!', 'info')
            return redirect(url_for('auth.login'))
        flash('错误的邮箱!', 'warning')
        return redirect(url_for('auth.forget_password'))
    return render_template('auth/reset_password.html', form=form)


# 重置密码(需携带QQ邮箱发送的token)
@auth_bp.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """
    验证重置密码的token
    :param token:
    :return:
    """
    # 判断当前用户是否登录
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    # 创建重置密码的表单
    form = ResetPasswordForm()
    if form.validate_on_submit():
        email = form.email.data.lower()
        # 新密码
        password = form.password.data
        # 通过email查找用户
        user = User.query.filter_by(email=email).first()
        if user:
            # 开始验证token
            if validate_token(user=user, token=token, operation=Operations.RESET_PASSWORD, new_password=password):
                flash("用户密码更新成功!", 'success')
                return redirect(url_for('auth.login'))
            else:
                flash("更新密码的token验证失败!", 'danger')
                return redirect(url_for('auth.forget_password'))
        else:
            return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


# 用户登出视图函数
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功!', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/captcha')
def captcha():
    c = Captcha()
    image, code = c.generate_captcha()
    # 创建一个缓冲区,用于保存二进制流
    buffer = BytesIO()
    image.save(buffer, 'jpeg')
    # 获取图片的二进制流
    image = buffer.getvalue()
    # 把buf_str作为response返回前端，并设置首部字段
    response = make_response(image)
    response.headers['Content-Type'] = 'image/gif'
    # 将验证码字符串储存在session中
    redis_db = RedisDb()
    redis_db.handle_captcha(code, code)
    print("redis存入的code1是: ", redis_db.handle_captcha(code))
    return response
