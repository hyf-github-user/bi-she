# coding:utf-8
# 作者：我只是代码的搬运工
# 文件名  :information_setting.py
# 时间    :2022/3/18 08:07
from django.contrib.auth import get_user_model
from rest_framework import serializers

Users = get_user_model()


class ChangePasswordSerializer(serializers.ModelSerializer):
    """
    个人中心修改密码序列化器
    """
    old_password = serializers.CharField(write_only=True, required=True)
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = Users
        fields = ['old_password', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {
                'required': True,
                'max_length': 20,
                'min_length': 6,
                'write_only': True,
                'error_messages': {
                    'max_length': '密码长度应在6 到 20位',
                    'min_length': '密码长度应在6 到 20位',
                }
            }
        }

    def validate(self, attrs):
        """
        重写校验方法
        :param attrs:
        :return:
        """
        if not self.instance.check_password(attrs.get('old_password')):
            raise serializers.ValidationError('原密码错误')
        if attrs.get('confirm_password') != attrs.get('password'):
            raise serializers.ValidationError('两次输入密码不一致')
        return attrs

    def update(self, instance, validated_data):
        """
        重写更新用户密码的方法
        :param instance:
        :param validated_data:
        :return:
        """
        self.instance.set_password(validated_data.get('password'))
        self.instance.save()
        return self.instance


class ChangeInformationSerializer(serializers.ModelSerializer):
    """
    个人中心修改个人信息序列化器
    """
    mobile = serializers.RegexField(r'^1[3-9]\d{9}$', allow_blank=True, error_messages={'invalid': '手机号格式错误'})

    class Meta:
        model = Users
        fields = ['name', 'mobile', 'email']

    @staticmethod
    def validate_mobile(mobile):
        # 避免字段为 '' 时 models unique约束失败
        if mobile == '':
            return None
        else:
            return mobile


class ChangeAvatarSerializer(serializers.ModelSerializer):
    """
    个人中心修改个人头像序列化器
    """

    class Meta:
        model = Users
        fields = ['image']
