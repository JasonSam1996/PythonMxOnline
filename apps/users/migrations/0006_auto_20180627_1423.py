# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 14:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_banner_emailcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailcode',
            name='send_time',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='发送时间'),
        ),
    ]
