import json
from pure_pagination import Paginator, PageNotAnInteger
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from users.forms import ModifyPwdForm
from users.models import UserProfile, EmailCode
from organization.models import CourseOrg, Teacher
from course.models import Course
from utils.mixin_utils import LoginRequiredMixin
from utils.email_send import send_email
from .forms import UploadImageForm, UserInfoForm
from .models import UserCourse, UserFavorite, UserMessage


# Create your views here.
class UserInfoView(LoginRequiredMixin, View):
    """
    个人资料
    """

    def get(self, request):
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "current_page": current_page
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class UploadImageView(LoginRequiredMixin, View):
    """
    修改头像
    """

    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(LoginRequiredMixin, View):
    """
    重置密码
    """

    def post(self, request):
        reset_form = ModifyPwdForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(reset_form.errors), content_type='application/json')


class SendEmailView(LoginRequiredMixin, View):
    """
    发送邮箱验证码
    """

    def get(self, request):
        email = request.GET.get("email", "")

        # 判断邮箱是否存在
        if UserProfile.objects.filter(email=email):
            return HttpResponse('{"email":"邮箱已经存在"}', content_type='application/json')

        send_email(email, "update_email")
        return HttpResponse('{"status":"success"}', content_type='application/json')


class UpdateEmailView(LoginRequiredMixin, View):
    """
    修改邮箱
    """

    def post(self, request):
        email = request.POST.get("email", "")
        code = request.POST.get("code", "")
        send_type = "update_email"

        existed_records = EmailCode.objects.filter(email=email, code=code, send_type=send_type)
        if existed_records:
            user = request.user
            user.email = email
            user.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"email":"验证码出错"}', content_type='application/json')


class MyCourseView(LoginRequiredMixin, View):
    """
    我的课程
    """

    def get(self, request):
        current_page = "mycourse"
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html", {
            "user_courses": user_courses,
            "current_page": current_page
        })


class MyFavOrgView(LoginRequiredMixin, View):
    def get(self, request):
        #  我的收藏——机构
        current_page = "myfav"
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, "usercenter-fav-org.html", {
            "current_page": current_page,
            "org_list": org_list
        })


class MyFavTeacherView(LoginRequiredMixin, View):
    def get(self, request):
        #  我的收藏——教师
        current_page = "myfav"
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=teacher_id)
            teacher_list.append(teacher)
        return render(request, "usercenter-fav-teacher.html", {
            "current_page": current_page,
            "teacher_list": teacher_list
        })


class MyFavCourseView(LoginRequiredMixin, View):
    def get(self, request):
        #  我的收藏——教师
        current_page = "myfav"
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        print(course_list)
        return render(request, "usercenter-fav-course.html", {
            "current_page": current_page,
            "course_list": course_list
        })


class MyMessageView(LoginRequiredMixin, View):
    def get(self, request):
        current_page = "mymessage"
        all_message = UserMessage.objects.filter(Q(user=request.user.id)|Q(user=0))
        # 分页功能
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 5, request=request)

        messages = p.page(page)
        return render(request, "usercenter-message.html", {
            "current_page": current_page,
            "messages": messages
        })
