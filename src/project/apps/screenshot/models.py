# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


# class OSPlatformBrowserVersion(models.Model):
#     readable_id = models.CharField(max_length=191, error_messages={'unique': "This name already existed."})
#     os_platform = models.CharField(max_length=191, choices=form_field_tuples.OS_PLATFORMS_LIST)
#     os_platform_version = models.CharField(max_length=191, blank=False, null=False)
#     browser = models.CharField(max_length=191, choices=form_field_tuples.BROWSERS_LIST, blank=False, null=False)
#     browser_version = models.CharField(max_length=191, blank=True, null=True)
#     device = models.CharField(max_length=191, choices=form_field_tuples.DEVICES_LIST, blank=True, null=True)
#     created_at = models.DateField(auto_now=False, auto_now_add=True)
#     updated_at = models.DateField(auto_now_add=False, auto_now=True)
#
#     class Meta:
#         unique_together = (('os_platform', 'os_platform_version', 'browser', 'browser_version', 'device'),)
#
#     def __str__(self):
#         return str(self.readable_id).replace('-', ' ')
#
#     def __unicode__(self):
#         return str(self.readable_id).replace('-', ' ')
#
#     def clean(self):
#
#         if self.os_platform == 'ios' or self.os_platform == 'android':
#             if self.device == '' or self.device is None:
#                 raise ValidationError('Mobile platform must provide a device name')
#
#             if not ((self.os_platform == 'ios' and self.browser == 'Mobile Safari') or
#                     (self.os_platform == 'android' and self.browser == 'Android Browser')):
#                 raise ValidationError('Mobile platform and device name does not match, (ios & Mobile Safari) or '
#                                       '(android & Android Browser)')
#
#             self.readable_id = self.os_platform + " " + self.os_platform_version + " " + self.device
#             self.readable_id = str(self.readable_id).replace(' ', '-')
#             self.browser_version = None
#
#         else:
#
#             if self.browser == 'Mobile Safari' or self.browser == 'Android Browser':
#                 raise ValidationError('Computer platform must not provide mobile browser.')
#
#             if self.os_platform == '' or self.os_platform_version == ''\
#                     or self.browser == '' or self.browser_version == ''\
#                     or self.os_platform is None or self.os_platform_version is None\
#                     or self.browser is None or self.browser_version is None:
#
#                 raise ValidationError('Computer platform, all fields are require except device.')
#
# self.readable_id = self.os_platform + " " + self.os_platform_version + " " + self.browser + " " + self.browser_version
#             self.readable_id = str(self.readable_id).replace(' ', '-')
#             self.device = None
#
#         duplicates = self.__class__.objects.filter(readable_id=self.readable_id).exclude(pk=self.pk)
#         if duplicates:
# raise ValidationError('OS Platform, OS version, Browser, Browser Version,  Device must be unique together.')
#
#     def save(self, *args, **kwargs):
#         super(OSPlatformBrowserVersion, self).save(*args, **kwargs)


class BrowserStackAvailableBrowser(models.Model):
    """
    All Browsers which available on BrowserStack.com was loaded and insert
    into this ORM model.

    Load browsers data from BrowserStack might be update every single day at a specific time
    in order to ensure the the matching rate between application and BrowserStack data
    """
    readable_name = models.CharField(max_length=255, blank=True, null=True)
    os_platform = models.CharField(max_length=15, blank=False, null=False)
    os_version = models.CharField(max_length=191, blank=False, null=False)
    browser = models.CharField(max_length=50, blank=False, null=False)
    browser_version = models.CharField(max_length=50, blank=True, null=True)
    device = models.CharField(max_length=191, blank=True, null=True)
    real_mobile = models.NullBooleanField(null=True)
    created_at = models.DateField(auto_now=False, auto_now_add=True)
    updated_at = models.DateField(auto_now_add=False, auto_now=True)

    class Meta:
        verbose_name = 'browser'
        verbose_name_plural = 'browsers'
        ordering = ('os_platform', 'os_version', 'browser')

    def __str__(self):
        return str(self.readable_name).replace('_', ' ')

    def __unicode__(self):
        return str(self.readable_name).replace('_', ' ')

    def save(self, *args, **kwargs):
        if isinstance(self.real_mobile, bool):
            real_mobile = 1 if self.real_mobile is True else 0
            self.readable_name = str(self.os_platform).replace(' ', '-') + " " + \
                                 str(self.os_version).replace(' ', '-') + " " + \
                                 str(self.browser).replace(' ', '-') + " " + \
                                 str(self.device).replace(' ', '-') + " " + \
                                 str(real_mobile)
            self.readable_name = str(self.readable_name).replace(' ', '_')
        else:
            self.readable_name = str(self.os_platform).replace(' ', '-') + " " + \
                                 str(self.os_version).replace(' ', '-') + " " + \
                                 str(self.browser).replace(' ', '-') + " " + \
                                 str(self.browser_version).replace(' ', '-')
            self.readable_name = str(self.readable_name).replace(' ', '_')
            
        super(BrowserStackAvailableBrowser, self).save(*args, **kwargs)
