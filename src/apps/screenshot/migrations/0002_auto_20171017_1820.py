# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 18:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('screenshot', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osplatformbrowserversion',
            name='readable_id',
            field=models.CharField(error_messages={'unique': 'This name already existed.'}, max_length=191, unique=True),
        ),
    ]
