# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-29 07:48
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0007_auto_20190928_0613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='registeredbundle',
            name='is_grouped',
        ),
        migrations.RemoveField(
            model_name='registeredbundle',
            name='pretest_score',
        ),
    ]
