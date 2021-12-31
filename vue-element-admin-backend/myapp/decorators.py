# 作者：我只是代码的搬运工
# coding:utf-8
# 实现禁止未登录的用户访问关键的视图
from functools import wraps
from flask import flash, url_for, redirect, abort, Markup, request, current_app
from flask_login import current_user
from myapp.utils.network import Result


def confirm_required(func):
    '''
    # 过滤未确认的用户
    # '''
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
                abort(403)
            return func(*args, **kwargs)
        return decorated_function
    return decorator


# 需要管理员身份的装饰器
def admin_required(func):
    return permission_required('ADMINISTER')(func)


def jwt_validate(f):
    """
    jwt验证的装饰器
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        # 获取前端发来的hear中的Authorization
        token = request.headers.get("Authorization", default=None)
        print("jwt的token:", token)
        from myapp.utils.token import identify
        user_info, status = identify(
            token, key=current_app.config.get('JWT_SECRET'))
        if not user_info or not status:
            print("jwt验证失败!")
            return Result.error(message="Token认证失败!")
        return f(*args, **kwargs)
    return wrapper
