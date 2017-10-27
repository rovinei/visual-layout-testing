from django.conf.urls import url

from .views import (ScreenshotFormView, ScreenshotJobAPI)

urlpatterns = [
    url(r'^$', ScreenshotFormView.as_view(), name='form'),
    url(r'^api/v.1/generate-screenshot', ScreenshotJobAPI.as_view(), name="api-request-screenshot")
]
