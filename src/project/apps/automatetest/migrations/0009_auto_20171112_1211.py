# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-12 12:11
from __future__ import unicode_literals

from django.db import migrations, models
import src.project.apps.automatetest.utils


class Migration(migrations.Migration):

    dependencies = [
        ('automatetest', '0008_auto_20171112_0015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specfile',
            name='spec_file',
            field=models.FileField(upload_to=src.project.apps.automatetest.utils.handle_upload_spec),
        ),
    ]
