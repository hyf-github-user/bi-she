# 作者：我只是代码的搬运工
# coding:utf-8

# 发送QQ邮箱请求
from threading import Thread

from flask import current_app, render_template
from flask_mail import Message

from exts import mail


def _send_async_mail(app, message):
    with app.app_context():
        mail.send(message)


def send_mail(to, subject, template, **kwargs):
    message = Message(current_app.config['BLUELOG_MAIL_SUBJECT_PREFIX'] + subject, recipients=[to])
    message.body = render_template(template + '.txt', **kwargs)
    message.html = render_template(template + '.html', **kwargs)
    app = current_app._get_current_object()  # 获取当前的User对象
    thr = Thread(target=_send_async_mail, args=[app, message])
    thr.start()
    return thr


# 发送确认邮件
def send_confirm_email(user, token, to=None):
    send_mail(subject='注册确认邮件', to=to or user.email, template='emails/confirm', user=user, token=token)


# 发送重置密码的确认邮件
def send_reset_password_email(user, token):
    send_mail(subject='重置密码', to=user.email, template='emails/reset_password', user=user, token=token)


# 发送改变邮箱的确认邮件
def send_change_email_email(user, token, to=None):
    send_mail(subject='确认修改邮箱', to=to or user.email, template='emails/change_email', user=user,
              token=token)
