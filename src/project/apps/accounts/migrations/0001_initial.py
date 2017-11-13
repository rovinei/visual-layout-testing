# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-06 10:01
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import src.project.apps.accounts.utils


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Username')),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Contact number')),
                ('address', models.CharField(blank=True, max_length=255, null=True, verbose_name='Current address')),
                ('state', models.CharField(blank=True, max_length=255, null=True, verbose_name='State/Origin')),
                ('city', models.CharField(blank=True, max_length=255, null=True, verbose_name='City')),
                ('country', models.CharField(blank=True, max_length=255, null=True, verbose_name='Country')),
                ('bio', models.TextField(default='', verbose_name='Biology')),
                ('date_of_birth', models.DateField(verbose_name='Date of birth')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to=src.project.apps.accounts.utils.handle_upload_avatar)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Last name')),
                ('username', models.CharField(blank=True, max_length=255, null=True, verbose_name='Username')),
                ('position', models.CharField(blank=True, max_length=191, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Phone number')),
                ('fax_number', models.CharField(blank=True, max_length=15, null=True, verbose_name='Fax')),
                ('avatar', models.ImageField(upload_to=src.project.apps.accounts.utils.handle_upload_avatar)),
                ('bio', models.TextField(blank=True, null=True, verbose_name='Background')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Registered Date')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated Date')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
