# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-16 11:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0009_auto_20180716_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classlist',
            name='start_date',
            field=models.DateField(auto_now_add=True, verbose_name='开班日期'),
        ),
    ]