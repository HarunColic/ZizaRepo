# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-08-16 23:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0002_auto_20180816_2302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 8, 16, 23, 6, 4, 787605)),
        ),
    ]
