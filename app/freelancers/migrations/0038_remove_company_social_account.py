# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-06-14 19:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0037_auto_20170611_0024'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='social_account',
        ),
    ]
