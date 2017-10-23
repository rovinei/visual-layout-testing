# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import OSPlatformBrowserVersion
from .forms import CreatePlatformBrowserForm
# Register your models here.


@admin.register(OSPlatformBrowserVersion)
class OSPlatformBrowserVersionAdmin(admin.ModelAdmin):
    form = CreatePlatformBrowserForm
    list_display = ('__str__', 'os_platform', 'os_platform_version', 'browser', 'device')
    empty_value_display = '--None--'
    list_filter = ('os_platform', 'os_platform_version', 'browser')
