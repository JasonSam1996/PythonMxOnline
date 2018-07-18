from django.conf.urls import url
from .views import UserInfoView, UploadImageView, UpdatePwdView, SendEmailView, UpdateEmailView, MyCourseView, \
    MyFavOrgView, MyFavTeacherView, MyFavCourseView, MyMessageView

urlpatterns = [
    # 个人信息
    url(r'^info/$', UserInfoView.as_view(), name='usercenter_info'),

    # 个人信息修改头像
    url(r'^image/upload/$', UploadImageView.as_view(), name='image_upload'),

    # 个人信息修改密码
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd'),

    # 发送邮箱验证码
    url(r'^sendemail_code/$', SendEmailView.as_view(), name='sendemail_code'),

    # 修改邮箱
    url(r'^update_email/$', UpdateEmailView.as_view(), name='update_email'),

    # 用户课程
    url(r'^my_course/$', MyCourseView.as_view(), name='my_course'),

    # 用户收藏机构
    url(r'^my_fav/org/$', MyFavOrgView.as_view(), name='my_fav_org'),

    # 用户收藏教师
    url(r'^my_fav/teacher/$', MyFavTeacherView.as_view(), name='my_fav_teacher'),

    # 用户收藏课程
    url(r'^my_fav/course/$', MyFavCourseView.as_view(), name='my_fav_course'),

    # 用户消息
    url(r'^my_message$', MyMessageView.as_view(), name='my_message$'),
]
