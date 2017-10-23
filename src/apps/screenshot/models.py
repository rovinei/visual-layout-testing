# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.core.exceptions import ValidationError
from .data import form_field_tuples


class OSPlatformBrowserVersion(models.Model):
    readable_id = models.CharField(max_length=191, unique=True, error_messages={'unique': "This name already existed."})
    os_platform = models.CharField(max_length=191, choices=form_field_tuples.OS_PLATFORMS_LIST)
    os_platform_version = models.CharField(max_length=191, blank=False, null=False)
    browser = models.CharField(max_length=191, choices=form_field_tuples.BROWSERS_LIST, blank=False, null=False)
    browser_version = models.CharField(max_length=191, blank=True, null=True)
    device = models.CharField(max_length=191, choices=form_field_tuples.DEVICES_LIST, blank=True, null=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        unique_together = (('os_platform', 'os_platform_version', 'browser', 'browser_version', 'device'),)

    def __str__(self):
        return str(self.readable_id).replace('-', ' ')

    def __unicode__(self):
        return str(self.readable_id).replace('-', ' ')

    def clean(self):

        if self.os_platform == 'ios' or self.os_platform == 'android':
            if self.device == '' or self.device is None:
                raise ValidationError('Mobile platform must provide a device name')

            if not ((self.os_platform == 'ios' and self.browser == 'Mobile Safari') or
                    (self.os_platform == 'android' and self.browser == 'Android Browser')):
                raise ValidationError('Mobile platform and device name does not match, (ios & Mobile Safari) or '
                                      '(android & Android Browser)')

            self.readable_id = self.os_platform + " " + self.os_platform_version + " " + self.device
            self.readable_id = str(self.readable_id).replace(' ', '-')
            self.browser_version = None

        else:

            if self.browser == 'Mobile Safari' or self.browser == 'Android Browser':
                raise ValidationError('Computer platform must not provide mobile browser.')

            if self.os_platform == '' or self.os_platform_version == ''\
                    or self.browser == '' or self.browser_version == ''\
                    or self.os_platform is None or self.os_platform_version is None\
                    or self.browser is None or self.browser_version is None:

                raise ValidationError('Computer platform, all fields are require except device.')

            self.readable_id = self.os_platform + " " + self.os_platform_version + " " + self.browser + " " + self.browser_version
            self.readable_id = str(self.readable_id).replace(' ', '-')
            self.device = None

        duplicates = self.__class__.objects.filter(readable_id=self.readable_id).exclude(pk=self.pk)
        if duplicates:
            raise ValidationError('OS Platform, OS version, Browser, Browser Version,  Device must be unique together.')

    def save(self, *args, **kwargs):
        super(OSPlatformBrowserVersion, self).save(*args, **kwargs)

