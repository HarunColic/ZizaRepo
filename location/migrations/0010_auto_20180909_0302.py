# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-09 03:02
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('location', '0009_auto_20180909_0258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2018, 9, 9, 3, 2, 45, 56405)),
        ),
    ]
