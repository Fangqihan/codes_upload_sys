# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-05 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_auto_20180705_0004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='url_type',
            field=models.SmallIntegerField(choices=[(0, 'absolute'), (1, 'dynamic')]),
        ),
    ]
