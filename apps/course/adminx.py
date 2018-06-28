import xadmin
from .models import Course, Lesson, Video, CourseRes


class CourseAdmin(object):
    pass


class LessonAdmin(object):
    pass


class VideoAdmin(object):
    pass


class CourseResAdmin(object):
    pass


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseRes,CourseResAdmin)