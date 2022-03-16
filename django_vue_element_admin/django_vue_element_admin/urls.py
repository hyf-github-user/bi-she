"""django_vue_element_admin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

# swagger接口文档配置
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(title="swaggerAPI文档",
                 default_version="v1",
                 description="API文档",
                 terms_of_service="",
                 contact=openapi.Contact(email="1348977728@qq.com"),
                 license=openapi.License(name="MIT")),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

base_api = settings.BASE_API
urlpatterns = [
    path('admin/', admin.site.urls),
    # 配置总路由
    # 项目模块
    path(f'{base_api}oauth/', include('django_vue_element_admin.myapps.oauth.urls')),  # 用户鉴权模块
    path(f'{base_api}system/', include('django_vue_element_admin.myapps.system.urls')),  # 系统管理模块
    path(f'{base_api}monitor/', include('django_vue_element_admin.myapps.monitor.urls')),  # 系统监控模块
    path(f'{base_api}boke/', include('django_vue_element_admin.myapps.boke.urls')),  # 博客前台
    # 配置swagger的配置
    url(r"swagger/", schema_view.with_ui("swagger",
                                         cache_timeout=0), name="schema-swagger"),
    url(r"redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
# 上传文件的路由
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
