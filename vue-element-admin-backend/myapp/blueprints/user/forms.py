# 作者：我只是代码的搬运工
# coding:utf-8

# 方便出现中文调试信息
from flask_ckeditor import CKEditorField
from flask_wtf import FlaskForm
from flask_mdeditor import MDEditorField
# 用户处理所需要的表单
from wtforms import TextAreaField, HiddenField, SubmitField, StringField, SelectField
from wtforms.validators import DataRequired, Email, Length, Optional, URL, ValidationError

from myapp.models.user import Category


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class PostForm(MyBaseForm):
    """
    文章表单
    """
    title = StringField('主题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int, default=1)
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]


# 评论表单
class CommentForm(MyBaseForm):
    body = TextAreaField('内容', validators=[DataRequired()])
    submit = SubmitField('发表')


class CategoryForm(MyBaseForm):
    """
    分类表单
    """
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    submit = SubmitField("创建")

    def validate_name(self, field):
        if Category.query.filter_by(name=field.data).first():
            raise ValidationError('分类已被创建!')


class LinkForm(MyBaseForm):
    """
    友情链接的表单
    """
    name = StringField('名称', validators=[DataRequired(), Length(1, 30)])
    url = StringField('网址', validators=[DataRequired(), URL(), Length(1, 255)])
    submit = SubmitField("创建")
