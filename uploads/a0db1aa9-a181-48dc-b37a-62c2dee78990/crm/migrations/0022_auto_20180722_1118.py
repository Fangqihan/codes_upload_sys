# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-22 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0021_auto_20180721_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='crm.StudentEnrollment'),
        ),
    ]