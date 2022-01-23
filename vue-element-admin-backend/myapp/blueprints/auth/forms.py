# 作者：我只是代码的搬运工
# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import Email, Length, DataRequired, Regexp, EqualTo, ValidationError
from myapp.models.user import User


# 方便出现中文调试信息
class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']


# 认证所需的表单
# 登录表单
class LoginForm(MyBaseForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 254, message="长度至少1位"),
                                            Email(message="必须是电子邮箱!")])
    password = PasswordField('密码', validators=[DataRequired()])
    remember_me = BooleanField('记住我登录')
    submit = SubmitField('登录')


# 注册表单
class RegisterForm(MyBaseForm):
    name = StringField('名称', validators=[DataRequired(), Length(1, 30, message="长度至少1位")])
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64, message="长度至少1位"),
                                            Email(message="必须是电子邮箱!")])
    username = StringField('用户名',
                           validators=[DataRequired(), Length(1, 20, message="长度至少1位"),
                                       Regexp('^[a-zA-z0-9]*$', message='用户名应该只包含a-z,'
                                                                        'A-Z 或者 0-9')])
    password = PasswordField('密码', validators=[DataRequired(), Length(8, 128, message="长度至少8位"),
                                               EqualTo('password2', message="俩次密码必须一致!")])
    password2 = PasswordField('确认密码', validators=[DataRequired()])
    submit = SubmitField('注册')

    # 验证邮箱
    def validate_email(self, field):
        if User.query.filter_by(email=field.data.lower()).first():
            raise ValidationError('电子邮件已被使用!')

    # 验证用户名
    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已被使用!')


# 忘记密码表单
class ForgetPasswordForm(MyBaseForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64, message="长度至少1位"),
                                            Email(message="必须是电子邮箱!")])

    submit = SubmitField('忘记密码')


# 重置密码表单
class ResetPasswordForm(MyBaseForm):
    email = StringField('电子邮件', validators=[DataRequired(), Length(1, 64, message="长度至少1位"),
                                            Email(message="必须是电子邮箱!")])
    password = PasswordField('密码', validators=[
        DataRequired(), Length(8, 128, message="长度至少8位"), EqualTo('password2', message="俩次密码不一致!")])

    password2 = PasswordField('确认密码', validators=[DataRequired()])

    submit = SubmitField("重置密码")
