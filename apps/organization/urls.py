from django.conf.urls import url

from .views import OrgListView, AddUserAskView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, AddFavView, \
    TeacherListView,TeacherDescView

urlpatterns = [
    # 课程机构
    url(r'^list/$', OrgListView.as_view(), name='org_list'),

    # 添加咨询
    url(r'^add_ask/$', AddUserAskView.as_view(), name='add_ask'),

    # 机构首页
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),

    # 机构课程
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),

    # 机构详情
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),

    # 机构讲师
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),

    # 添加收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav'),

    # 授课教师
    url(r'^teacher/list/$', TeacherListView.as_view(), name='taecher_list'),

    # 教师详情
    url(r'^teacher/desc/(?P<teacher_id>\d+)/$', TeacherDescView.as_view(), name='taecher_desc'),

]
