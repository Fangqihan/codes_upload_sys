# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 15:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0016_contracttemplate_class_grade'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracttemplate',
            name='class_grade',
        ),
    ]
