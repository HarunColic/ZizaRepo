# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-09-30 15:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0016_post_views'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='type',
            field=models.IntegerField(default=1),
        ),
    ]
