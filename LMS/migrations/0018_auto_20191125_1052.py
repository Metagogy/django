# -*- coding: utf-8 -*-
# Generated by Django 1.11.25 on 2019-11-25 10:52
from __future__ import unicode_literals

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0017_subtag_course'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subtag',
            name='topic',
            field=smart_selects.db_fields.GroupedForeignKey(blank=True, group_field='course', null=True, on_delete=django.db.models.deletion.CASCADE, to='LMS.Topic'),
        ),
    ]
