# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-09 15:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0007_auto_20180709_2327'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customerinfo',
            options={'verbose_name': '客户信息', 'verbose_name_plural': '客户信息'},
        ),
    ]
