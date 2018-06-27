from django.db import models
from datetime import datetime


# Create your models here.

class CityDict(models.Model):
    name = models.CharField(max_length=20, verbose_name=u"城市")
    desc = models.CharField(max_length=200, verbose_name=u"描述")
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u"城市信息"
        verbose_name_plural = verbose_name


class CourseOrg(models.Model):
    name = models.CharField(max_length=50, verbose_name=u'机构名称')
    desc = models.TextField(verbose_name=u'机构描述')
    chick_nums = models.IntegerField(default=0, verbose_name=u'点击数量')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏数量')
    image = models.ImageField(upload_to='org/%Y/%m', max_length=100, verbose_name=u'机构封面')
    address = models.CharField(max_length=100, verbose_name=u'机构地址')
    city = models.ForeignKey(CityDict, verbose_name=u'所在城市')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'机构信息'
        verbose_name_plural = verbose_name


class Teacher(models.Model):
    org = models.ForeignKey(CourseOrg, verbose_name=u'所在机构')
    name = models.CharField(max_length=50, verbose_name=u'教师名称')
    work_year = models.IntegerField(default=0, verbose_name=u'工作年龄')
    work_company = models.CharField(max_length=50, verbose_name=u'就职公司')
    work_position = models.CharField(max_length=50, verbose_name=u'工作职位')
    points = models.CharField(max_length=100,verbose_name=u'教学特点')
    chick_nums = models.IntegerField(default=0,verbose_name=u'点击人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'教师信息'
        verbose_name_plural = verbose_name
