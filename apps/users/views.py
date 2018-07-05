from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.db.models import Q

from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyPwdForm
from .models import UserProfile, EmailCode
from utils.email_send import send_email


# Create your views here.

class CustomBackend(ModelBackend):
    """
    实现邮箱用户名通用登录
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class ActiveCodeView(View):
    """
    获取图片验证码
    """
    def get(self, request, active_code):
        # 数据库查询验证码
        all_code = EmailCode.objects.filter(code=active_code)
        # 判断是否有验证码，如果有就循环查询发送的邮箱，并且把is_active设置为True，然后保存数据库
        if all_code:
            for code in all_code:
                email = code.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, "active_failure.html", {})
        return render(request, "login.html", {})


class RegisterView(View):
    """
    注册功能
    """
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {'register_form': register_form})

    def post(self, request):
        # 实例化form，验证每个字段是否合法
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            # 取出邮箱
            user_name = request.POST.get('email', '')
            # 判断用户名是否存在
            if UserProfile.objects.filter(email=user_name):
                return render(request, "register.html", {"register_form": register_form, "msg": "用户名已经存在"})
            # 取出密码
            pass_word = request.POST.get('password', '')
            # 实例化用户，然后赋值提交到数据库，但用户未激活
            user_profile = UserProfile()
            user_profile.username = user_name
            user_profile.email = user_name
            user_profile.is_active = False
            user_profile.password = make_password(pass_word)
            user_profile.save()

            # 发送到用户邮箱并且叫用户激活
            send_email(user_name, "register")
            return HttpResponseRedirect(reverse("login"))
        else:
            return render(request, "register.html", {"register_form": register_form})


class LoginView(View):
    """
    登录功能
    """
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        # 实例化登录form，验证每个字段是否合法
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            # 取出username和password并实例化user
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            user = authenticate(username=user_name, password=pass_word)
            # 判断user是否有值，有则登录，没有则提示错误
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse("index"))
                else:
                    return render(request, "login.html", {'msg': '用户未激活！'})
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误！'})
        else:
            return render(request, "login.html", {"login_form": login_form})


class ForgetPwdView(View):
    """
    忘记密码功能
    """
    def get(self, request):
        forgetpwd_form = ForgetPwdForm()
        return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})

    def post(self, request):
        forgetpwd_form = ForgetPwdForm(request.POST)
        if forgetpwd_form.is_valid():
            email = request.POST.get('email', '')
            send_email(email, "forget")
            return render(request, "send_success.html", {})
        else:
            return render(request, "forgetpwd.html", {"forgetpwd_form": forgetpwd_form})


class ResetView(View):
    """
    打开重置密码页面
    """
    def get(self, request, active_code):
        # 数据库查询验证码
        all_code = EmailCode.objects.filter(code=active_code)
        # 判断是否有验证码，如果有就循环查询发送的邮箱，并且把is_active设置为True，然后保存数据库
        if all_code:
            for code in all_code:
                email = code.email
                return render(request, "password_reset.html", {"email": email})
        else:
            return render(request, "active_failure.html", {})
        return render(request, "login.html")


class ModifyPwdView(View):
    """
    重置密码
    """
    def post(self, request):
        reset_form = ModifyPwdForm(request.POST)
        if reset_form.is_valid():
            pwd1 = request.POST.get('password1', '')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email', '')
            if pwd1 != pwd2:
                return render(request, "password_reset.html", {"email": email, 'msg': '密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return HttpResponseRedirect(reverse("login"))
        else:
            email = request.POST.get('email', '')
            return render(request, "password_reset.html", {"email": email, 'reset_form': reset_form})
