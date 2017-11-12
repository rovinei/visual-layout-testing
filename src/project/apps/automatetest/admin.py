# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Project,
    TestBuild,
    TestSession,
    ScreenshotImage,
    GalenReport,
    SpecFile
)

from .forms import ProjectCreationForm


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    form = ProjectCreationForm
    list_display = ('__str__', 'owner', 'project_uuid', 'created_at')
    empty_value_display = '--None--'

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        super(ProjectAdmin, self).save_model(request, obj, form, change)


@admin.register(TestBuild)
class TestBuildAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = '--None--'


@admin.register(TestSession)
class TestSessionAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = '--None--'


@admin.register(GalenReport)
class GalenReportAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'created_at')
    empty_value_display = '--None--'


@admin.register(ScreenshotImage)
class ScreenshotAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = '--None--'


@admin.register(SpecFile)
class SpecFileAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'project', 'spec_file')
    empty_value_display = '--None--'