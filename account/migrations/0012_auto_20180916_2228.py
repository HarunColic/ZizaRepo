# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-16 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0013_auto_20180915_2346'),
        ('account', '0011_auto_20180909_1619'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='industryID',
        ),
        migrations.AddField(
            model_name='company',
            name='categoryID',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='post.Category'),
        ),
    ]
