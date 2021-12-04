# 作者：我只是代码的搬运工
# coding:utf-8
from flask import Blueprint
from flask_login import login_required

auth_bp = Blueprint("auth_bp", __name__)


# 用户登录视图函数
@auth_bp.route('/login', methods=['POST', 'GET'])
def login():
    pass


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
    pass
