# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-29 15:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0023_auto_20170511_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default=111, upload_to='pictures/%Y/%m/%d/'),
            preserve_default=False,
        ),
    ]
