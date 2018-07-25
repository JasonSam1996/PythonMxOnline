"""PythonMxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from users.views import LoginView, RegisterView, ActiveCodeView, ForgetPwdView, ResetView, ModifyPwdView, LogoutView, \
    IndexView
from django.views.static import serve
from PythonMxOnline.settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveCodeView.as_view(), name='user_active'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget_pwd'),
    url(r'^reset/(?P<active_code>.*)/$', ResetView.as_view(), name='reset_pwd'),
    url(r'^modify/$', ModifyPwdView.as_view(), name='modify_pwd'),

    # 课程机构列表
    url(r'^org/', include('organization.urls', namespace='org')),
    # 课程列表
    url(r'^course/', include('course.urls', namespace='course')),
    # 个人中心
    url(r'^usercenter/', include('operation.urls', namespace='usercenter')),

    # 上传文件路径
    url(r'^media/(?P<path>.*)/$', serve, {"document_root": MEDIA_ROOT}),

    # 静态文件路径
    # url(r'^static/(?P<path>.*)/$', serve, {"document_root": STATIC_ROOT }),

    # 富文本
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

handler404 = 'users.views.page_not_fount'

handler500 = 'users.views.server_error'
