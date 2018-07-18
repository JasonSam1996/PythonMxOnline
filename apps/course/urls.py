from django.conf.urls import url
from .views import CourseListView, CourseDescView, CourseInfoView, CourseCommentView, AddCommentView,VideoPlayView

urlpatterns = [
    # 课程机构
    url(r'^list/$', CourseListView.as_view(), name='course_list'),

    # 课程详情
    url(r'^desc/(?P<course_id>\d+)/$', CourseDescView.as_view(), name='course_desc'),

    # 课程章节
    url(r'^info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),

    # 课程评论
    url(r'^comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),

    # 添加评论
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),

    # 课程视频
    url(r'^video/(?P<video_id>\d+)/$', VideoPlayView.as_view(), name='video_play'),


]
