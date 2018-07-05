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
    pass


xadmin.site.register(UserAsk, UserAskAdmin)
xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
