"""webAutomateTesting URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from project import views

urlpatterns = [
    url(r'^$', views.redirect_view, name="root-domain"),
    url(r'^admin/', admin.site.urls),
    url(r'^clarifai/', include('project.apps.clarifaiApi.urls', namespace='clarifai-api')),
    url(r'^screenshot/', include('project.apps.screenshot.urls', namespace="screenshot-app"), name="screenshot-app")
]
