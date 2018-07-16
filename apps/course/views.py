from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.db.models import Q
from pure_pagination import Paginator, PageNotAnInteger
from .models import Course, CourseRes, Video
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


# Create your views here.


class CourseListView(View):
    """
    课程列表页
    """

    def get(self, request):
        all_course = Course.objects.all().order_by("-add_time")
        hot_course = all_course.order_by('-chick_nums')[:3]

        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_course = all_course.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords) | Q(
                detail__icontains=search_keywords))

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_course = all_course.order_by("-chick_nums")
            elif sort == 'students':
                all_course = all_course.order_by("-students")

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_course, 5, request=request)

        course = p.page(page)

        return render(request, "course-list.html", {
            "all_course": course,
            "hot_course": hot_course,
            "sort": sort,
        })


class CourseDescView(View):
    """
    课程详情页
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 增加点击数
        course.chick_nums += 1
        course.save()

        has_fav_course = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                has_fav_course = True

            if UserFavorite.objects.filter(user=request.user, fav_id=course.course_org.id, fav_type=2):
                has_fav_org = True

        tag = course.tag
        if tag:
            releta_courses = Course.objects.filter(tag=tag)[:1]
        else:
            releta_courses = []
        return render(request, "course-detail.html", {
            "course": course,
            "releta_courses": releta_courses,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    """
    课程章节信息
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))

        course.students += 1
        course.save()

        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # model用法 user_id__in是个列表
        # 取出所有课程id
        courses_id = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过其他的课程
        relate_courses = Course.objects.filter(id__in=courses_id).order_by("-chick_nums")[:5]
        all_courseres = CourseRes.objects.filter(course=course)
        return render(request, "course-video.html", {
            "course": course,
            "all_courseres": all_courseres,
            "relate_courses": relate_courses,
        })


class CourseCommentView(LoginRequiredMixin, View):
    """
    课程评论显示
    """

    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_courseres = CourseRes.objects.filter(course=course)
        all_comment = CourseComments.objects.all()
        return render(request, "course-comment.html", {
            "course": course,
            "all_courseres": all_courseres,
            "all_comment": all_comment,
        })


class AddCommentView(View):
    """
    添加课程评论
    """

    def post(self, request):
        if not request.user.is_authenticated():
            # 判断用户的登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")

        course_id = request.POST.get("course_id", 0)
        comments = request.POST.get("comments", "")
        if int(course_id) > 0 and comments:
            course_comment = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comment.course = course
            course_comment.comment = comments
            course_comment.user = request.user
            course_comment.save()
            return HttpResponse('{"status":"success","msg":"添加成功"}', content_type="application/json")
        else:
            return HttpResponse('{"status":"fail","msg":"添加失败"}', content_type="application/json")


class VideoPlayView(View):
    def get(self, request, video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course
        course.students += 1
        course.save()

        user_course = UserCourse.objects.filter(user=request.user, course=course)
        if not user_course:
            user_course = UserCourse(user=request.user, course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # model用法 user_id__in是个列表
        # 取出所有课程id
        courses_id = [user_course.course.id for user_course in all_user_courses]
        # 获取该用户学过其他的课程
        relate_courses = Course.objects.filter(id__in=courses_id).order_by("-chick_nums")[:5]
        all_courseres = CourseRes.objects.filter(course=course)
        return render(request, "course-play.html", {
            "course": course,
            "all_courseres": all_courseres,
            "relate_courses": relate_courses,
            "video": video
        })
