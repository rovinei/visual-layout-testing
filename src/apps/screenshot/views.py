# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse
from django.views.generic.base import View
from django.conf import settings
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as selenium_exception
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium import webdriver

from .forms import ScreenshotAPIForm
from .models import OSPlatformBrowserVersion

import time
import os

from .util import (random_string)

HUB_URL = 'http://localhost:4444/wd/hub'
MOBILE_EMULATION_LIST = [
    {"deviceName": "iPhone 3GS"},
    {"deviceName": "iPhone 4"},
    {"deviceName": "iPhone 5"},
    {"deviceName": "iPhone 6"},
    {"deviceName": "iPhone 6 Plus"},
    {"deviceName": "BlackBerry Z10"},
    {"deviceName": "BlackBerry Z30"},
    {"deviceName": "Nexus 4"},
    {"deviceName": "Nexus 5"},
    {"deviceName": "Nexus S"},
    {"deviceName": "HTC Evo, Touch HD, Desire HD, Desire"},
    {"deviceName": "HTC One X, EVO LTE"},
    {"deviceName": "HTC Sensation, Evo 3D"},
    {"deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black"},
    {"deviceName": "LG Optimus G"},
    {"deviceName": "LG Optimus LTE, Optimus 4X HD"},
    {"deviceName": "LG Optimus One"},
    {"deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900"},
    {"deviceName": "Galaxy Note 3"},
    {"deviceName": "Galaxy Note II"},
    {"deviceName": "Galaxy Note"},
    {"deviceName": "Galaxy S III, Galaxy Nexus"},
    {"deviceName": "Galaxy S, S II, W"},
    {"deviceName": "Galaxy S4"},
    {"deviceName": "Xperia S, Ion"},
    {"deviceName": "Xperia Sola, U"},
    {"deviceName": "Xperia Z, Z1"},
    {"deviceName": "Amazon Kindle Fire HDX 7″"},
    {"deviceName": "Amazon Kindle Fire HDX 8.9″"},
    {"deviceName": "Amazon Kindle Fire (First Generation)"},
    {"deviceName": "iPad 1 / 2 / iPad Mini"},
    {"deviceName": "iPad 3 / 4"},
    {"deviceName": "BlackBerry PlayBook"},
    {"deviceName": "Nexus 10"},
    {"deviceName": "Nexus 7 2"},
    {"deviceName": "Nexus 7"},
    {"deviceName": "Motorola Xoom, Xyboard"},
    {"deviceName": "Galaxy Tab 7.7, 8.9, 10.1"},
    {"deviceName": "Galaxy Tab"},
    {"deviceName": "Notebook with touch"},

    # Or specify a specific build using the following two arguments
    # "deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
    # "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
]


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

        all_browsers = OSPlatformBrowserVersion.objects.all()
        os_versions = all_browsers.values('os_platform', 'os_platform_version').distinct()
        for os_item in os_versions:
            os_obj = dict()
            browsers = all_browsers.filter(
                os_platform=os_item['os_platform'],
                os_platform_version=os_item['os_platform_version']).order_by('os_platform')
            browser_versions = browsers.values('browser').distinct()

            browser_arr = list()
            for b in browser_versions:
                brows = dict()
                brows_items = browsers.filter(browser=b['browser']).order_by('browser')
                browser_icon_url = "screenshot/custom/img/icons/svg/"+str(b['browser']).strip(" ").replace(" ", "-").lower()+".svg"
                brows.update({
                    'browser_name': b['browser'],
                    'icon_url': browser_icon_url,
                    'browser_versions': brows_items
                })
                browser_arr.append(brows)

            os_name = os_item['os_platform'] + ' ' + os_item['os_platform_version']
            icon_url = "screenshot/custom/img/icons/svg/"+str(os_item['os_platform']).strip(" ").replace(" ", "-").lower()+".svg"
            os_obj.update({
                'os_name': os_name,
                'os_platform': os_item['os_platform'],
                'icon_url': icon_url,
                'browsers': browser_arr
            })
            os_arr.append(os_obj)

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


class ScreenshotJobAPI(View):

    def get(self, request):
        contexts = dict()
        contexts.update({
            'page_info': {
                'title': 'Automate Screenshot API | Potential United',
                'meta': {
                    'keyword': 'Automate testing, cross browser testing, visual regression testing, website layout test'
                }
            }
        })
        return render(request, 'screenshot/screenshot_form.html', contexts)

    def post(self, request):

        chrome_options = webdriver.ChromeOptions()
        page_url = request.POST.get('page_url')
        mac_res = request.POST.get('mac_res')
        win_res = request.POST.get('win_res')
        screenshot_quality = request.POST.get('screenshot_quality')
        browsers = request.POST.getlist('browsers')
        os_platform, os_version, browser, device_or_browser_version = browsers[0].split('|')

        capabilities = DesiredCapabilities.CHROME.copy()

        if os_platform.lower() == 'os x':
            capabilities['platform'] = "MAC"
            capabilities['version'] = device_or_browser_version
            driver = webdriver.Remote(command_executor=HUB_URL,
                                      desired_capabilities=capabilities)

        elif os_platform.lower() == 'windows':
            capabilities['platform'] = "WINDOWS"
            capabilities['version'] = device_or_browser_version
            driver = webdriver.Remote(command_executor=HUB_URL,
                                      desired_capabilities=capabilities)

        elif os_platform.lower() == 'android' or os_platform.lower() == 'ios':
            mobile_emulation = {"deviceName": device_or_browser_version}
            chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
            driver = webdriver.Remote(command_executor=HUB_URL,
                                      desired_capabilities=chrome_options.to_capabilities())
        driver.get(page_url)
        driver.maximize_window()
        random_str = random_string(64)
        img_path = os.path.join(settings.MEDIA_ROOT, "projects/punited/"+random_str+".png")
        time.sleep(3)

        try:
            status_screenshot = driver.save_screenshot(img_path)
            if status_screenshot:
                return JsonResponse({"status": "200", "img_path": img_path})
            else:
                return JsonResponse({"status": "500", "error_message": "Failed to capture screenshot"})
        except selenium_exception.WebDriverException as webExe:
            print(webExe.msg)
            return JsonResponse({"status": "500", "error_message": "Failed to capture screenshot"})
        finally:
            driver.quit()
