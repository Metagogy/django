# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-27 04:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0002_quizresult'),
    ]

    operations = [
        migrations.AddField(
            model_name='pretest',
            name='bundle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LMS.Bundle'),
        ),
    ]
