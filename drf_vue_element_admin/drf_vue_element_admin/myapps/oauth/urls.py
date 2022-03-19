from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token

from drf_vue_element_admin.myapps.oauth.views import oauth

urlpatterns = [
    # 用户登录视图
    path('login/', oauth.UserLoginView.as_view()),
    # 用户登出视图
    path('logout/', oauth.LogoutAPIView.as_view()),
    # 刷新token视图
    path('refresh/', refresh_jwt_token),
    # 获取用户信息的视图
    path('info/', oauth.UserInfoView.as_view()),
]
