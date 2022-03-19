from flask import url_for

from exts import db
from myapp.models.user import Notification


def push_follow_notification(follower, receiver):
    message = '用户 <a href="%s">%s</a> 刚刚关注了你!' % \
              (url_for('user.index', username=follower.username), follower.username)
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


def push_comment_notification(post_id, receiver, page=1):
    message = '<a href="%s#comments">这篇文章</a> 刚刚有了最新评论或回复.' % \
              (url_for('main.show_post', post_id=post_id, page=page))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()


def push_collect_notification(collector, post_id, receiver):
    message = '用户 <a href="%s">%s</a> 刚刚收藏了你的 <a href="%s">文章</a>' % \
              (url_for('user.index', username=collector.username),
               collector.username,
               url_for('main.show_post', post_id=post_id))
    notification = Notification(message=message, receiver=receiver)
    db.session.add(notification)
    db.session.commit()
