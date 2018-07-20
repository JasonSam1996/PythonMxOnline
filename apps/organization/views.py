from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q
from operation.models import UserFavorite
from .forms import UserAskForm
from .models import CourseOrg, CityDict, Teacher
from course.models import Course


# Create your views here.

class OrgListView(View):
    def get(self, request):
        """展示课程机构列表，筛选，"""
        # 课程机构
        all_orgs = CourseOrg.objects.all()

        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords) | Q(desc__icontains=search_keywords))

        # 城市列表
        all_city = CityDict.objects.all()

        # 授课机构排名筛选
        hot_org = all_orgs.order_by('-chick_nums')[:3]

        # 取出筛选所在城市
        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        # 取出筛选机构类别
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by("-students")
            elif sort == 'courses':
                all_orgs = all_orgs.order_by("-course_nums")

        # 筛选出一共有多少家机构
        org_nums = all_orgs.count()

        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 5, request=request)

        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs': orgs,
            'all_city': all_city,
            'org_nums': org_nums,
            'city_id': city_id,
            'category': category,
            'hot_org': hot_org,
            'sort': sort,
        })


class AddUserAskView(View):
    def post(self, request):
        """
            用户添加咨询
        """
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail","msg":"添加出错"}', content_type="application/json")


class OrgHomeView(View):
    """
    机构首页
    """

    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.chick_nums += 1
        course_org.save()
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
            'has_fav': has_fav,
        })


class OrgCourseView(View):
    """
    机构课程
    """

    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_courses = course_org.course_set.all()
        return render(request, "org-detail-course.html", {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgDescView(View):
    """机构介绍"""

    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
            "has_fav": has_fav,
        })


class OrgTeacherView(View):
    """
    机构讲师
    """

    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        has_fav = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "course_org": course_org,
            "all_teacher": all_teacher,
            "current_page": current_page,
            "has_fav": has_fav
        })


class AddFavView(View):
    """
        用户收藏，用户取消收藏
    """

    def post(self, request):
        # 取出用户收藏的id和收藏类型
        fav_id = request.POST.get('fav_id', 0)
        fav_type = request.POST.get('fav_type', 0)

        if not request.user.is_authenticated():
            # 判断用户的登录状态
            return HttpResponse('{"status":"fail","msg":"用户未登录"}', content_type="application/json")

        exist_records = UserFavorite.objects.filter(user=request.user, fav_id=int(fav_id), fav_type=int(fav_type))
        if exist_records:
            # 如果已经存在，则用户取消收藏
            exist_records.delete()
            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            elif int(fav_type) == 2:
                org = CourseOrg.objects.get(id=int(fav_id))
                org.fav_nums -= 1
                if org.fav_nums < 0:
                    org.fav_nums = 0
                org.save()
            elif int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()
            return HttpResponse('{"status":"success","msg":"收藏"}', content_type="application/json")
        else:
            # 如果不存在，则用户收藏
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()
                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                elif int(fav_type) == 2:
                    org = CourseOrg.objects.get(id=int(fav_id))
                    org.fav_nums += 1
                    org.save()
                elif int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()
                return HttpResponse('{"status":"success","msg":"已收藏"}', content_type="application/json")
            else:
                return HttpResponse('{"status":"fail","msg":"收藏出错"}', content_type="application/json")


class TeacherListView(View):
    def get(self, request):
        all_teacher = Teacher.objects.all()

        search_keywords = request.GET.get("keywords", "")
        if search_keywords:
            all_teacher = all_teacher.filter(
                Q(name__icontains=search_keywords) | Q(work_company__icontains=search_keywords) | Q(
                    work_position__icontains=search_keywords))

        # 讲师排行榜
        hot_teacher = all_teacher.order_by('-chick_nums')[:3]
        sort = request.GET.get('sort', '')
        if sort:
            if sort == 'hot':
                all_teacher = all_teacher.order_by("-chick_nums")
        # 分页功能
        teacher_nums = all_teacher.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_teacher, 5, request=request)

        teachers = p.page(page)
        return render(request, "teachers-list.html", {
            "all_teacher": teachers,
            "teacher_nums": teacher_nums,
            "hot_teacher": hot_teacher,
            "sort": sort,
        })


class TeacherDescView(View):
    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(id=teacher_id)
        teacher.chick_nums += 1
        teacher.save()
        courses = teacher.course_set.all()
        hot_teacher = Teacher.objects.all().order_by('-chick_nums')[:3]
        has_fav_teacher = False
        has_fav_org = False

        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.id, fav_type=3):
                has_fav_teacher = True

            if UserFavorite.objects.filter(user=request.user, fav_id=teacher.org.id, fav_type=2):
                has_fav_org = True
        return render(request, "teacher-detail.html", {
            "teacher": teacher,
            "courses": courses,
            "hot_teacher": hot_teacher,
            "has_fav_teacher": has_fav_teacher,
            "has_fav_org": has_fav_org
        })
