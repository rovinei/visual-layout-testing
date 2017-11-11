# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import uuid
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from .utils import upload_screenshot
from project.settings.storage_backend import MediaStorage
from django.contrib.auth.models import User


class Project(models.Model):
    """"
    Test project
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    project_uuid = models.CharField(max_length=64, unique=True)
    project_name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'project'
        verbose_name_plural = 'projects'
        ordering = ('created_at',)

    def __str__(self):
        return self.project_name

    def __unicode__(self):
        return self.project_name

    def save(self, *args, **kwargs):
        def generate_uid():
            gen_uid = str(uuid.uuid4()).replace('-', '')
            print(gen_uid)
            return gen_uid

        def existed(identifier):
            project = self.__class__.objects.filter(project_uuid=identifier).first()
            return project

        def check_existed_uid():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_uid()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.project_uuid = uid
            print(self.project_uuid)
        if self.project_uuid is None or self.project_uuid == '':
            check_existed_uid()
        super(Project, self).save(*args, **kwargs)


class TestBuild(models.Model):
    """"
    Test build version of a project
    """
    name = models.CharField(max_length=255)
    build_uuid = models.CharField(max_length=64, unique=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='builds')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            build = self.__class__.objects.filter(build_uuid=identifier).first()
            return build

        def check_existed_uid():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_uid()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.build_uuid = uid

        if self.build_uuid is None or self.build_uuid == '':
            check_existed_uid()
        super(TestBuild, self).save(*args, **kwargs)


class TestSession(models.Model):
    """"
    Session uuid return from selenium or browser stack, which
    belonged to a specific build's project
    """

    title = models.CharField(max_length=255, blank=True, null=True)
    session_uuid = models.CharField(max_length=64, unique=True)
    build = models.ForeignKey(TestBuild, on_delete=models.CASCADE, related_name='sessions')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='sessions')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.title).capitalize()

    def __unicode__(self):
        return str(self.title).capitalize()

    def save(self, *args, **kwargs):
        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            session = self.__class__.objects.filter(session_uuid=identifier).first()
            return session

        def check_existed_uid():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_uid()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.session_uuid = uid

        if self.session_uuid is None or self.session_uuid == '':
            check_existed_uid()
        super(TestSession, self).save(*args, **kwargs)


class GalenReport(models.Model):
    """
    Report reference generate by Galen Framework
    """
    report_uuid = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, default='')
    report_dir = models.CharField(max_length=500)
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, related_name='reports', null=True)
    build = models.ForeignKey(TestBuild, on_delete=models.SET_NULL, related_name='reports', null=True)
    session = models.ForeignKey(TestSession, on_delete=models.SET_NULL, related_name='reports', null=True)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.title).capitalize()

    def __unicode__(self):
        return str(self.title).capitalize()

    def save(self, *args, **kwargs):
        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            report = self.__class__.objects.filter(report_uuid=identifier).first()
            return report

        def check_existed_uid():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_uid()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.report_uuid = uid

        if self.report_uuid is None or self.report_uuid == '':
            check_existed_uid()
        super(GalenReport, self).save(*args, **kwargs)


class ScreenshotImage(models.Model):
    """"
    Screenshot images
    """
    screenshot_uuid = models.CharField(max_length=64, unique=True)
    src = models.ImageField(upload_to=upload_screenshot, storage=MediaStorage)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='screenshots')
    build = models.ForeignKey(TestBuild, on_delete=models.CASCADE, related_name='screenshots')
    session = models.ForeignKey(TestSession, on_delete=models.CASCADE, related_name='screenshots')
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return str(self.title).capitalize()

    def __unicode__(self):
        return str(self.title).capitalize()

    def save(self, *args, **kwargs):
        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            image = self.__class__.objects.filter(screenshot_uuid=identifier).first()
            return image

        def check_existed_uid():
            uid = generate_uid()
            if existed(uid):
                try:
                    check_existed_uid()
                except RuntimeError:
                    raise ValidationError(
                        "Unique id is existed, already retried to the maximum time, Please resubmit the form."
                    )

            self.screenshot_uuid = uid

        if self.screenshot_uuid is None or self.screenshot_uuid == '':
            check_existed_uid()
        super(ScreenshotImage, self).save(*args, **kwargs)
