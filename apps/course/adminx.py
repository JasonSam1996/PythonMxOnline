import xadmin
from .models import Course, Lesson, Video, CourseRes


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                    'chick_nums', 'chick_nums', 'image', 'course_org', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                     'chick_nums', 'chick_nums', 'image', 'course_org']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                   'chick_nums', 'chick_nums', 'image', 'course_org', 'add_time']


class LessonAdmin(object):
    pass


class VideoAdmin(object):
    pass


class CourseResAdmin(object):
    pass


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseRes, CourseResAdmin)
