# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-11 18:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0007_course_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='course_information',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='课程须知'),
        ),
        migrations.AddField(
            model_name='course',
            name='learn_what',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='学到什么'),
        ),
    ]
