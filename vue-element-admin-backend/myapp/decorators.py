# 作者：我只是代码的搬运工
# coding:utf-8
# 实现禁止未登录的用户访问关键的视图
from functools import wraps

from flask import flash, url_for, redirect, abort, Markup
from flask_login import current_user, logout_user


def confirm_required(func):
    """
    # 过滤未确认的用户
    # """

    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirmed:
            message = Markup(
                '请先确认你的邮件!'
                '没有收到邮件吗?'
                '<a class="alert-link" href="%s">重新发送邮件</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)

    return decorated_function


# 权限验证装饰器
def permission_required(permission_name):
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission_name):
                # 如果不具有权限
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator

def check_locked(func):
    """
    # 过滤锁定的用户
    # """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.role.name == "locked":
            flash("你的账号已被封禁!", "warning")
            logout_user()
        return func(*args, **kwargs)
    return decorated_function
