# 作者：我只是代码的搬运工
# coding:utf-8
import os
from datetime import datetime

from flask import Blueprint, request, render_template, url_for, jsonify, Response, current_app, send_from_directory, \
    flash, redirect
from flask_login import current_user

from exts import csrf, db
from myapp.models.user import Post

user_bp = Blueprint("user", __name__)


@user_bp.route('/post/new', methods=['GET', 'POST'])
@csrf.exempt  # 忽略csrf保护
def new_post():
    if request.method == 'GET':
        return render_template('editormd_post/new_post.html')
    else:
        title = request.form['title']
        body = request.form['content']
        body_html = request.form['fancy-editormd-html-code']
        post = Post(title=title, body=body, body_html=body_html, author=current_user._get_current_object())
        db.session.add(post)
        db.session.commit()
        flash("文章已发表!", 'success')
        return redirect(url_for('auth.login'))


@user_bp.route('/post/upload', methods=['POST'])
@csrf.exempt
def upload():
    file = request.files.get('editormd-image-file')
    if not file:
        res = {
            'success': 0,
            'message': '上传失败'
        }
    else:
        ex = os.path.splitext(file.filename)[1]
        filename = datetime.now().strftime('%Y%m%d%H%M%S') + ex
        file.save(os.path.join(current_app.config['PHOTO_SAVE_PATH'], filename))
        res = {
            'success': 1,
            'message': '上传成功',
            'url': url_for('.image', filename=filename)
        }
    return jsonify(res)


@user_bp.route('/post/image/<filename>')
def image(filename):
    return send_from_directory(current_app.config['PHOTO_SAVE_PATH'], filename=filename)


@user_bp.route('/post/<int:post_id>/show')
def show_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    if post:
        title = post.title
        body = post.body
        body_html = post.body_html
        print(body)
        return render_template('editormd_post/show_post.html', post=post)
