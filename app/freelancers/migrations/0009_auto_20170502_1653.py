# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-02 16:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0008_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='experiences',
            field=models.ManyToManyField(null=True, to='freelancers.Experience'),
        ),
    ]