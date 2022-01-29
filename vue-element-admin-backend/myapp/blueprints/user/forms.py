# 作者：我只是代码的搬运工
# coding:utf-8

# 方便出现中文调试信息
from flask_wtf import FlaskForm

# 用户处理所需要的表单
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class PostForm(MyBaseForm):
    body = TextAreaField('Body', [DataRequired()])
    body_html = HiddenField()
    submit = SubmitField("发布")
