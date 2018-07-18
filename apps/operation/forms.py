from django import forms
from users.models import UserProfile


class UploadImageForm(forms.ModelForm):
    """
    使用modelform实现添加用户咨询
    """

    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    """
    使用modelform实现添加用户咨询
    """

    class Meta:
        model = UserProfile
        fields = ['nick_name','birday','gender','address','phone']
