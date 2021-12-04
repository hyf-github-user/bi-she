# 作者：我只是代码的搬运工
# coding:utf-8


# 方便出现中文调试信息
from flask_wtf import FlaskForm


# 评论所需要的表单
class MyBaseForm(FlaskForm):
    class Meta:
        locales = ['zh']