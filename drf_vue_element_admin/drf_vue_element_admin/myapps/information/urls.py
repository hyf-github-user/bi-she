from django.urls import path

from drf_vue_element_admin.myapps.information.views import information_setting

urlpatterns = [
    path('change-password/', information_setting.ChangePasswordAPIView.as_view()),  # 修改个人密码
    path('change-information/', information_setting.ChangeInformationAPIView.as_view()),  # 修改个人信息
    path('change-avatar/', information_setting.ChangeAvatarAPIView.as_view()),  # 修改个人头像
]
