import json
from django.shortcuts import render
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from users.forms import ModifyPwdForm
from utils.mixin_utils import LoginRequiredMixin
from .forms import UploadImageForm


# Create your views here.
class UserInfoView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "usercenter-info.html", {
        })


class UploadImageView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
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
