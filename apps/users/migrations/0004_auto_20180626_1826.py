# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-26 10:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(upload_to='user/image/%Y/%m', verbose_name='头像'),
        ),
    ]
