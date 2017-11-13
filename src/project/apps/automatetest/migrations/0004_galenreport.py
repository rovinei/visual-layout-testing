# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-10 04:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('automatetest', '0003_auto_20171110_0405'),
    ]

    operations = [
        migrations.CreateModel(
            name='GalenReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('report_uuid', models.CharField(max_length=64, unique=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
                ('description', models.TextField(blank=True, default='')),
                ('report_dir', models.CharField(max_length=500)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]