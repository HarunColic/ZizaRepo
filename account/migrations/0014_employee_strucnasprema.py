# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-17 16:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0013_employee_editovanprofil'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='strucnaSprema',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
