# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :forms.py
# 时间    :2021/12/31 11:52
# 评论表单
from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class CommentForm(MyBaseForm):
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发表')
