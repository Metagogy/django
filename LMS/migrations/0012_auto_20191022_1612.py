# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-22 16:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0011_question_timegiven'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='timetaken',
            field=models.FloatField(blank=True, default=0.0, null=True),
        ),
    ]