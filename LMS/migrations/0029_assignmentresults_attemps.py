# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-12-12 09:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0028_auto_20191212_0908'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignmentresults',
            name='attemps',
            field=models.IntegerField(default=0),
        ),
    ]