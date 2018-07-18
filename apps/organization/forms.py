from django import forms

from operation.models import UserAsk

import re


class UserAskForm(forms.ModelForm):
    """
    使用modelform实现添加用户咨询
    """

    class Meta:
        model = UserAsk
        fields = ['name', 'phone', 'course_name']

    def clean_phone(self):
        """
            验证手机号是否合法
        :return: 手机号
        """
        phone = self.cleaned_data['phone']
        REGEX_PHONE = '^(13\d|14[5|7]|15\d|166|17[3|6|7]|18\d)\d{8}$'
        p = re.compile(REGEX_PHONE)
        if p.match(phone):
            return phone
        else:
            raise forms.ValidationError(u'请输入正确的手机号！', code='phone_invalid')
