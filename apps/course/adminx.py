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
    list_display = ['name', 'course', 'add_time']
    search_fields = ['name', 'course']
    list_filter = ['name', 'course', 'add_time']


class VideoAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson', 'add_time']


class CourseResAdmin(object):
    list_display = ['name', 'course', 'download', 'add_time']
    search_fields = ['name', 'course', 'download']
    list_filter = ['name', 'course', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseRes, CourseResAdmin)
