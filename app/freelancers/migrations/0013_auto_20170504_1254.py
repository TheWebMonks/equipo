# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-04 12:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0012_project_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='project',
            old_name='freelancers',
            new_name='profiles',
        ),
    ]