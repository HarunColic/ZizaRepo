# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-09 03:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0009_auto_20180909_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 50258)),
        ),
        migrations.AlterField(
            model_name='faq',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 53483)),
        ),
        migrations.AlterField(
            model_name='industry',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 48581)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 49474)),
        ),
        migrations.AlterField(
            model_name='postcategories',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 52352)),
        ),
        migrations.AlterField(
            model_name='posttags',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 51713)),
        ),
        migrations.AlterField(
            model_name='tag',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 50693)),
        ),
        migrations.AlterField(
            model_name='usercategories',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 52924)),
        ),
        migrations.AlterField(
            model_name='workersposts',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 51145)),
        ),
    ]
