from django.db import models
from datetime import datetime

from organization.models import CourseOrg,Teacher


# Create your models here.
class Course(models.Model):
    DEGREE_CHOICES = (
        (u'primary', u'初级'),
        (u'intermediate', u'中级'),
        (u'expert', u'高级'),
    )
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True)
    name = models.CharField(max_length=100, verbose_name=u'课程名称')
    desc = models.CharField(max_length=200, verbose_name=u'课程描述')
    detail = models.TextField(verbose_name=u'课程详情')
    teacher = models.ForeignKey(Teacher,verbose_name=u'讲师',null=True, blank=True)
    degree = models.CharField(choices=DEGREE_CHOICES, default='primary', max_length=15, verbose_name=u'课程难度')
    learn_time = models.IntegerField(default=1, verbose_name=u'学习时长')
    students = models.IntegerField(default=0, verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name=u'收藏人数')
    chick_nums = models.IntegerField(default=0, verbose_name=u'点击人数')
    image = models.FileField(upload_to='course/%Y/%m', max_length=100, verbose_name='封面')
    category = models.CharField(default="后端开发", max_length=20, verbose_name=u'课程类别')
    tag = models.CharField(default="", verbose_name=u'课程标签', max_length=10)
    course_information = models.CharField(max_length=300,verbose_name=u'课程须知',null=True, blank=True)
    learn_what = models.CharField(max_length=300,verbose_name=u'学到什么',null=True, blank=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程信息'
        verbose_name_plural = verbose_name

    def get_zj_nums(self):
        # 获取课程章节数
        return self.lesson_set.all().count()

    def get_learn_users(self):
        # 获取学习用户
        return self.usercourse_set.all()

    def get_course_lesson(self):
        # 获取课程所有章节
        return self.lesson_set.all()

    def __str__(self):
        return self.name


class Lesson(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=10, verbose_name=u'章节名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节信息'
        verbose_name_plural = verbose_name

    def get_lesson_video(self):
        # 获取章节所有视频
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson, verbose_name=u'章节')
    name = models.CharField(max_length=20, verbose_name=u'视频信息')
    url = models.URLField(default="", max_length=200, verbose_name=u'访问地址')
    learn_time = models.IntegerField(default=1, verbose_name=u'视频长度')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseRes(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程')
    name = models.CharField(max_length=20, verbose_name=u'资源名称')
    download = models.FileField(upload_to='course/res/%Y/%m', max_length=100, verbose_name=u'下载地址')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
