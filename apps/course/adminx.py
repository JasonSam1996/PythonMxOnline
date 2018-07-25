import xadmin
from .models import Course, Lesson, Video, CourseRes, BannerCourse


class LessonInLine(object):
    model = Lesson
    extra = 0


class CourseResInLine(object):
    model = CourseRes
    extra = 0


class CourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                    'chick_nums', 'chick_nums', 'image', 'course_org', 'get_zj_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                     'chick_nums', 'chick_nums', 'image', 'course_org']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                   'chick_nums', 'chick_nums', 'image', 'course_org', 'add_time']
    inlines = [LessonInLine, CourseResInLine]

    style_fields = {'detail': 'ueditor'}

    import_excel = True

    # 重写queryset过滤出不是轮播数据
    def queryset(self):
        qs = super(CourseAdmin, self).queryset()
        qs = qs.filter(is_banner=False)
        return qs

    def save_models(self):
        # 在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self, request, *args, **kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin, self).post(request, args, kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                    'chick_nums', 'chick_nums', 'image', 'course_org', 'get_zj_nums', 'add_time']
    search_fields = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                     'chick_nums', 'chick_nums', 'image', 'course_org']
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students', 'fav_nums',
                   'chick_nums', 'chick_nums', 'image', 'course_org', 'add_time']
    inlines = [LessonInLine, CourseResInLine]

    # 重写queryset过滤出轮播数据
    def queryset(self):
        qs = super(BannerCourseAdmin, self).queryset()
        qs = qs.filter(is_banner=True)
        return qs


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
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseRes, CourseResAdmin)
