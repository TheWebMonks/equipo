# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-07-12 11:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0041_auto_20170712_1108'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='name',
            field=models.CharField(default='Not Changed Yet! Please change the name A.S.A.P.', max_length=100),
            preserve_default=False,
        ),
    ]