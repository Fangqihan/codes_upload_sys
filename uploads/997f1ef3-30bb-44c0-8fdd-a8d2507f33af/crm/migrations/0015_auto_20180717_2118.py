# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-17 13:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0014_auto_20180717_1009'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customerinfo',
            name='age',
            field=models.IntegerField(blank=True, null=True, verbose_name='年龄'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='contact_info',
            field=models.CharField(max_length=64, unique=True, verbose_name='联系电话'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='date',
            field=models.DateField(auto_now_add=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='emergency_contact',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='紧急电话'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='gender',
            field=models.IntegerField(blank=True, choices=[(0, '男'), (1, '女')], null=True, verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='id_num',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='身份证号码'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='name',
            field=models.CharField(default=None, max_length=64, verbose_name='姓名'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='source',
            field=models.SmallIntegerField(choices=[(0, 'QQ群'), (1, '51CTO'), (2, '知乎'), (3, '转介绍'), (4, '百度推广'), (5, '其他')], verbose_name='来源'),
        ),
        migrations.AlterField(
            model_name='customerinfo',
            name='status',
            field=models.SmallIntegerField(choices=[(0, '未报名'), (1, '已报名'), (2, '已退学')], default=0, verbose_name='状态'),
        ),
        migrations.AlterModelTable(
            name='contracttemplate',
            table='合同',
        ),
        migrations.AlterModelTable(
            name='paymentrecord',
            table='缴费记录',
        ),
        migrations.AlterModelTable(
            name='studentenrollment',
            table='学生报名',
        ),
    ]
