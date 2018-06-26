from django.db import models
from datetime import datetime


# Create your models here.
class Course(models.Model):
    DEGREE_CHOICES = (
        (u'primary', u'初级'),
        (u'intermediate', u'中级'),
        (u'expert', u'高级'),
    )
    name = models.CharField(max_length=100, verbose_name=u'课程名称')
    desc = models.CharField(max_length=200, verbose_name=u'课程描述')
    detail = models.CharField(max_length=500, verbose_name=u'课程详情')
    degree = models.CharField(choices=DEGREE_CHOICES, default='primary', max_length=15, verbose_name=u'课程难度')
    learn_time = models.IntegerField(default=1, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    chick_nums = models.IntegerField(default=0, verbose_name=u'点击人数')
    image = models.FileField(upload_to='course/%Y/%m', max_length=100, verbose_name='封面')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程信息'
        verbose_name_plural = verbose_name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=10, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=20, verbose_name=u'视频信息')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name


class CourseRes(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=20, verbose_name=u'资源名称')
    download = models.FileField(upload_to='course/res/%Y/%m', max_length=100, verbose_name=u'下载地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name
