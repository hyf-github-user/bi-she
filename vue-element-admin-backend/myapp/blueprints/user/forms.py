# 作者：我只是代码的搬运工
# coding:utf-8

# 方便出现中文调试信息
from flask_ckeditor import CKEditorField
from flask_login import current_user
from flask_wtf import FlaskForm
# 用户处理所需要的表单
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import TextAreaField, SubmitField, StringField, SelectField, PasswordField, BooleanField, FileField, \
    HiddenField
from wtforms.validators import DataRequired, Length, Optional, URL, ValidationError, Regexp, EqualTo, Email

from myapp.models.user import Category, User


class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


class PostForm(MyBaseForm):
    """
    文章表单
    """
    _status = [('1', 'published'), ('2', 'draft')]
    _auth = [('1', '一般'), ('2', '重要'), ('2', '非常重要')]
    title = StringField('主题', validators=[DataRequired(), Length(1, 60)])
    category = SelectField('分类', coerce=int, default=1)
    status = SelectField('状态', choices=_status, default=1)
    auth = SelectField('重要性', choices=_auth, default=1)
    body = CKEditorField('内容', validators=[DataRequired()])
    submit = SubmitField('发布')

    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.category.choices = [(category.id, category.name)
                                 for category in Category.query.order_by(Category.name).all()]





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


class EditProfileForm(MyBaseForm):
    """
    编辑个人信息的表单
    """
    name = StringField('用户名', validators=[DataRequired(), Length(1, 30)])
    username = StringField('登录名', validators=[DataRequired(), Length(1, 20),
                                              Regexp('^[a-zA-Z0-9]*$',
                                                     message='登录名应该包含 a-z, A-Z 和 0-9.')])
    website = StringField('个人网站', validators=[Optional(), Length(0, 255)])
    submit = SubmitField('更新')

    def validate_username(self, field):
        """
        判断用户名是否重复
        :param field:
        :return:
        """
        if field.data != current_user.username and User.query.filter_by(username=field.data).first():
            raise ValidationError('这个用户名已经被使用!')


class ChangePasswordForm(MyBaseForm):
    old_password = PasswordField('旧密码', validators=[DataRequired()])
    password = PasswordField('新密码', validators=[
        DataRequired(), Length(8, 128), EqualTo('password2')])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('更新密码')


class ChangeEmailForm(MyBaseForm):
    email = StringField('新的邮箱', validators=[DataRequired(), Length(1, 254), Email()])
    submit = SubmitField('更新邮箱')

    def validate_email(self, field):
        """
        验证邮箱地址的是否被使用
        :param field:
        :return:
        """
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('这个邮箱地址已被使用!')


class NotificationSettingForm(MyBaseForm):
    """
    通知设置表单
    """
    receive_comment_notification = BooleanField('评论通知')
    receive_follow_notification = BooleanField('关注通知')
    receive_collect_notification = BooleanField('收藏通知')
    submit = SubmitField('确认更新')


class PrivacySettingForm(MyBaseForm):
    """
    设置收藏隐私的表单
    """
    public_collections = BooleanField('公开我的收藏')
    submit = SubmitField('确认更新')


class DeleteAccountForm(MyBaseForm):
    """
    注销用户的表单
    """
    username = StringField('用户名', validators=[DataRequired(), Length(1, 20)])
    submit = SubmitField()

    def validate_username(self, field):
        if field.data != current_user.username:
            raise ValidationError('错误的用户名')


class UploadAvatarForm(MyBaseForm):
    """
    上传头像的表单
    """
    image = FileField('上传头像', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], '图片格式只能是png或jpg')
    ])
    submit = SubmitField('更新头像')


class CropAvatarForm(MyBaseForm):
    """
    收集裁剪的头像表单
    """
    x = HiddenField()
    y = HiddenField()
    w = HiddenField()
    h = HiddenField()
    submit = SubmitField('裁剪并更新')
