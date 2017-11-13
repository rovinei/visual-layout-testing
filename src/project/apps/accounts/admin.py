# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import (
    Employee,
    Customer,
)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__', '__avatar_img__')
    empty_value_display = '--None--'


@admin.register(Customer)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    empty_value_display = '--None--'

