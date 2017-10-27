# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import uuid


class Project(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project_uuid = models.UUIDField()
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

    def clean(self):

        def generate_uid():
            return str(uuid.uuid4()).replace('-', "")

        def existed(identifier):
            project = self.objects.filter(project_uuid=identifier).first()
            return None not in project

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

        check_existed_uid()

    def save(self, *args, **kwargs):
        super(self, Project).save(*args, **kwargs)


# class TestSession(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
#
#
# class Report(models.Model):
#     project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True)
