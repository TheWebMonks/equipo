# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-05-07 19:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('freelancers', '0016_remove_project_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='company',
            field=models.ForeignKey(default=5, on_delete=django.db.models.deletion.CASCADE, to='freelancers.Company'),
            preserve_default=False,
        ),
    ]
