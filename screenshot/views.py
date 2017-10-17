# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from selenium.common import exceptions as selenium_exception
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import unittest
import time

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


class Screenshot(object):

    def index(self, request):
        contexts = dict()
        contexts.update({
            'page_info': {
                'title': 'Automate Screenshot API | Potential United',
                'meta': {
                    'keyword': 'Automate testing, cross browser testing, visual regression testing, website layout test'
                }
            }
        })

        if request.method == 'POST':
            print ""

        return JsonResponse(contexts)