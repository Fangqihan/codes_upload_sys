# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 15:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0015_auto_20180717_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='contracttemplate',
            name='class_grade',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='crm.ClassList', verbose_name='合同'),
        ),
    ]
