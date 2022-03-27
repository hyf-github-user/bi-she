from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path

# swagger接口文档配置
from django.views.decorators.clickjacking import xframe_options_exempt
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
    path('api/admin/', admin.site.urls),
    # 配置总路由
    # 项目模块
    path(f'{base_api}oauth/', include('drf_vue_element_admin.myapps.oauth.urls')),  # 用户鉴权模块
    path(f'{base_api}monitor/', include('drf_vue_element_admin.myapps.monitor.urls')),  # 系统监控模块
    path(f'{base_api}blog/', include('drf_vue_element_admin.myapps.blog.urls')),  # 博客前台
    path(f'{base_api}information/', include('drf_vue_element_admin.myapps.information.urls')),  # 用户中心
    # 配置swagger的配置
    re_path(rf'^{base_api}swagger(?P<format>\.json|\.yaml)$',
            xframe_options_exempt(schema_view.without_ui(cache_timeout=0)), name='schema-json'),
    path(f'{base_api}swagger/',
         xframe_options_exempt(schema_view.with_ui('swagger', cache_timeout=0)), name='schema-swagger-ui'),
    path(f'{base_api}redoc/',
         xframe_options_exempt(schema_view.with_ui('redoc', cache_timeout=0)), name='schema-redoc'),
]
# 上传文件的路由
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
