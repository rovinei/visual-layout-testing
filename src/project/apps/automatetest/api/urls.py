from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/v.1/generate-screenshot', views.get_browsers, name="api-get-browsers")

]
