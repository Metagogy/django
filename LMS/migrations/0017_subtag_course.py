# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-25 10:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0016_auto_20191028_1511'),
    ]

    operations = [
        migrations.AddField(
            model_name='subtag',
            name='course',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LMS.Course'),
        ),
    ]