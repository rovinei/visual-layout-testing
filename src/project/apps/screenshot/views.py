# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from django.conf import settings
from .forms import ScreenshotAPIForm
from .models import BrowserStackAvailableBrowser
from galenpy.galen_webdriver import GalenRemoteWebDriver
from galenpy.galen_api import (Galen, generate_galen_report)
from galenpy.galen_report import TestReport
from galenpy.exception import (FileNotFoundError, IllegalMethodCallException)
import time
import os
from .util import (random_string)


class ScreenshotFormView(View):

    def get(self, request):
        contexts = dict()
        os_arr = list()
        contexts.update({
            'page_info': {
                'title': 'Automate Screenshot API | Potential United',
                'meta': {
                    'keyword': 'Automate testing, cross browser testing, visual regression testing, website layout test'
                }
            }
        })

        all_browsers = BrowserStackAvailableBrowser.objects.all()
        os_versions = all_browsers.order_by('-os_platform', '-os_version').values('os_platform', 'os_version').distinct()
        if os_versions.exists():
            print(len(os_versions))
            
            for os_item in os_versions:
                os_obj = dict()
                browsers = all_browsers.filter(
                    os_platform=os_item['os_platform'],
                    os_version=os_item['os_version'])
                browser_versions = browsers.values('browser').distinct()
                browser_arr = list()
                for bs in browser_versions:
                    brows = dict()
                    brows_items = browsers.filter(browser=bs['browser'])
                    browser_icon_url = "screenshot/custom/img/icons/svg/"+str(bs['browser']).strip(" ").replace(" ", "-").lower()+".svg"
                    brows.update({
                        'browser_name': bs['browser'],
                        'icon_url': browser_icon_url,
                        'browser_versions': brows_items
                    })
                    browser_arr.append(brows)

                os_name = os_item['os_platform'] + ' ' + os_item['os_version']
                icon_url = "screenshot/custom/img/icons/svg/"+str(os_item['os_platform']).strip(" ").replace(" ", "-").lower()+".svg"
                os_obj.update({
                    'os_name': os_name,
                    'os_platform': os_item['os_platform'],
                    'icon_url': icon_url,
                    'browsers': browser_arr
                })
                os_arr.append(os_obj)

            contexts.update({'os_browsers': os_arr})
        else:
            contexts.update({'os_browsers': os_arr})

        screenshot_form = ScreenshotAPIForm(
            initial={
                'mac_res': '1149x768',
                'win_res': '1149x768',
                'screenshot_quality': 'original',
                'page_url': 'https://www.p-united.com'
            }
        )

        contexts.update({
            'screenshot_form': screenshot_form
        })
        return render(request, 'screenshot/screenshot_form.html', contexts)




