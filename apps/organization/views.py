from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from pure_pagination import Paginator, PageNotAnInteger

from .models import CourseOrg, CityDict
from .forms import UserAskForm
from operation.models import Course


# Create your views here.

class OrgListView(View):
    def get(self, request):
        """展示课程列表，筛选，"""
        # 课程机构
        all_orgs = CourseOrg.objects.all()
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
            'sort': sort
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
    def get(self, request, org_id):
        current_page = "home"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-homepage.html", {
            "all_courses": all_courses,
            "all_teacher": all_teacher,
            "course_org": course_org,
            "current_page": current_page,
        })


class OrgCourseView(View):
    def get(self, request, org_id):
        current_page = "course"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_courses = course_org.course_set.all()
        return render(request, "org-detail-course.html", {
            "all_courses": all_courses,
            "course_org": course_org,
            "current_page": current_page,
        })


class OrgDescView(View):
    def get(self, request, org_id):
        current_page = "desc"
        course_org = CourseOrg.objects.get(id=int(org_id))
        return render(request, "org-detail-desc.html", {
            "course_org": course_org,
            "current_page": current_page,
        })


class OrgTeacherView(View):
    def get(self, request, org_id):
        current_page = "teacher"
        course_org = CourseOrg.objects.get(id=int(org_id))
        all_teacher = course_org.teacher_set.all()
        return render(request, "org-detail-teachers.html", {
            "course_org": course_org,
            "all_teacher": all_teacher,
            "current_page": current_page,
        })
