# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-27 14:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='citydict',
            options={'verbose_name': '城市信息', 'verbose_name_plural': '城市信息'},
        ),
    ]
