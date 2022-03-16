from django.urls import path
from rest_framework_jwt.views import refresh_jwt_token
from django_vue_element_admin.myapps.oauth.views import oauth

urlpatterns = [
    # 查询用户登录成功之后显示的设备的信息
    # path('home/', home.HomeAPIView.as_view()),
    # 用户登录视图
    path('login/', oauth.UserLoginView.as_view()),
    # 用户登出视图
    path('logout/', oauth.LogoutAPIView.as_view()),
    # 刷新token视图
    path('refresh/', refresh_jwt_token),
    # 获取用户信息的视图
    path('info/', oauth.UserInfoView.as_view()),
]
