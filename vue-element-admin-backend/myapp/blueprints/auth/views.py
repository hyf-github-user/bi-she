# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint, flash, redirect, url_for, render_template
from flask_login import current_user, login_required, login_user, logout_user
from myapp.models.user import User
from myapp.blueprints.auth.forms import LoginForm

auth_bp = Blueprint("auth", __name__)


# 用户登录视图函数
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
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
    return render_template('main/login.html', form=form)


# 用户注册视图函数
@auth_bp.route('/register', methods=['POST', 'GET'])
def register():
    pass


# 用户刷新重新认证
@auth_bp.route('/re_authenticate', methods=['POST', 'GET'])
def re_authenticate():
    pass


# 通过token确认注册
@auth_bp.route('/confirm/<token>')
def confirm(token):
    pass


# 重写发送验证邮箱
@auth_bp.route('/resend-confirm-email')
def resend_confirm_email():
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
