# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-04 13:56
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_auto_20180704_1950'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='student',
        ),
    ]
