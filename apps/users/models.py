from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class UserProfile(AbstractUser):
    GENDER_CHOICES = (
        (u'M', u'男'),
        (u'F', u'女'),
    )
    nick_name = models.CharField(max_length=10, verbose_name=u'昵称')
    birday = models.DateField(verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=2, verbose_name=u'性别', default='M')
    address = models.CharField(max_length=200, verbose_name=u'地址')
    phone = models.CharField(max_length=11, verbose_name=u'电话号码')
    image = models.ImageField(verbose_name=u'头像', upload_to='user/image/%Y/%m', max_length=100)

    class Meta:
        verbose_name = u'用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class EmailCode(models.Model):
    SENDTYPE = (
        (u'register', u'注册'),
        (u'find', u'找回密码'),
    )
    code = models.CharField(max_length=10, verbose_name=u'验证码')
    email = models.CharField(max_length=50, verbose_name=u'邮箱')
    send_type = models.CharField(choices=SENDTYPE, verbose_name=u'验证类型', max_length=10)
    send_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name


class Banner(models.Model):
    title = models.CharField(max_length=100, verbose_name=u'标题')
    image = models.ImageField(verbose_name=u'封面', upload_to='userBanner/%Y/%m', max_length=100)
    url = models.URLField(verbose_name=u'访问地址')
    index = models.IntegerField(default=100, verbose_name=u'图片序号')
    add_time = models.DateTimeField(default=datetime.now)

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name
