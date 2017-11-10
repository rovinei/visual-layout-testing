from django.conf.urls import url

from .views import (ScreenshotFormView)

urlpatterns = [
    url(r'^$', ScreenshotFormView.as_view(), name='form'),
]
