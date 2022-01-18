# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user, logout_user

from exts import db
from myapp.models.user import User
from myapp.blueprints.auth.forms import LoginForm, RegisterForm
from myapp.utils import redirect_back
from myapp.utils.emails import send_confirm_email
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
def re_authenticate():
    pass


# 忘记密码视图函数
@auth_bp.route('/forget-password', methods=['POST', 'GET'])
def forget_password():
    pass


# 重置密码(需携带QQ邮箱发送的token)
@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    pass


# 用户登出视图函数
@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('登出成功!', 'info')
    return redirect(url_for('main.index'))
