# -*- coding: utf-8 -*-
# Generated by Django 1.11.24 on 2019-09-30 04:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Support', '0005_auto_20190929_0720'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='about',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.AlterField(
            model_name='query',
            name='query',
            field=models.TextField(blank=True, max_length=100000, null=True),
        ),
    ]