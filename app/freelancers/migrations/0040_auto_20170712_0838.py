# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-12 08:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0039_auto_20170712_0832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='price',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='expendedtime',
            name='start_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='expendedtime',
            name='stop_time',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='expendedtime',
            name='time',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.FloatField(default=0.0),
        ),
        migrations.AlterField(
            model_name='kindoftask',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
