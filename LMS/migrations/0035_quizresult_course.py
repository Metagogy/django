# -*- coding: utf-8 -*-
# Generated by Django 1.11.26 on 2020-01-11 12:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0034_assignmentresults_rewards'),
    ]

    operations = [
        migrations.AddField(
            model_name='quizresult',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LMS.Course'),
        ),
    ]