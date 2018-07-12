import xadmin
from .models import UserAsk, CourseComments, UserFavorite, UserMessage, UserCourse


class UserAskAdmin(object):
    pass


class CourseCommentsAdmin(object):
    pass


class UserFavoriteAdmin(object):
    pass


class UserMessageAdmin(object):
    pass


class UserCourseAdmin(object):
    list_display = ['user', 'course', 'add_time']
    search_fields = ['user', 'course']
    list_filter = ['user', 'course', 'add_time']


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
