# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-10-28 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0015_auto_20191028_1439'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='subtags',
        ),
        migrations.AddField(
            model_name='problem',
            name='subtags',
            field=models.ManyToManyField(blank=True, null=True, to='LMS.SubTag'),
        ),
        migrations.AlterField(
            model_name='subtag',
            name='content',
            field=models.TextField(blank=True, max_length=1000000, null=True),
        ),
    ]