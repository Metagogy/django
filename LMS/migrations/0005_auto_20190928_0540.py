# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-28 05:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0004_group_bundle'),
    ]

    operations = [
        migrations.CreateModel(
            name='BundleGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CourseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='group',
            name='bundle',
        ),
        migrations.RemoveField(
            model_name='group',
            name='course',
        ),
        migrations.RemoveField(
            model_name='group',
            name='user',
        ),
    ]