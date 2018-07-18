# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-17 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20180628_1611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcode',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码'), ('update_email', '修改邮箱')], max_length=15, verbose_name='验证类型'),
        ),
    ]
