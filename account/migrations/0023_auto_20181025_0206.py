# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-10-25 00:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0022_company_web'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='cv',
            field=models.FileField(max_length=1000, null=True, upload_to=''),
        ),
    ]
