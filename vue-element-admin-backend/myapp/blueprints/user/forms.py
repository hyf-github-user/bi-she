# 作者：我只是代码的搬运工
# coding:utf-8

# 方便出现中文调试信息
from flask_wtf import FlaskForm
from flask_mdeditor import MDEditorField
# 用户处理所需要的表单
from wtforms import TextAreaField, HiddenField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, URL

from myapp.models.user import Category


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']



# 评论表单
class CommentForm(MyBaseForm):
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发表')
