# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-11 00:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0036_auto_20170607_1806'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='description',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='place',
            field=models.CharField(default='Venezuela', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='city',
            field=models.CharField(default='Caracas', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.CharField(default='Venezuela', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='resume',
            field=models.CharField(default='jenny ondoline', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='profile',
            name='telephone',
            field=models.CharField(default='+123456789', max_length=100),
            preserve_default=False,
        ),
    ]
