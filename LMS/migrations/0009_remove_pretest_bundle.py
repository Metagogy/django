# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-29 07:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0008_auto_20190929_0748'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pretest',
            name='bundle',
        ),
    ]
