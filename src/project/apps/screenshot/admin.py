# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import BrowserStackAvailableBrowser
from .forms import CreateBrowserForm


@admin.register(BrowserStackAvailableBrowser)
class OSPlatformBrowserVersionAdmin(admin.ModelAdmin):
    form = CreateBrowserForm
    list_display = ('__str__', 'os_platform', 'os_version', 'browser', 'device')
    empty_value_display = '--None--'
    list_filter = ('os_platform', 'os_version', 'browser')
