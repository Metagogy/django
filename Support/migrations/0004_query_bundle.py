# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-28 06:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0007_auto_20190928_0613'),
        ('Support', '0003_auto_20190928_0540'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='bundle',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='LMS.Bundle'),
        ),
    ]
