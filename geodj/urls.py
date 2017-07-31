"""geodj URL Configuration

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
from django.conf.urls import url,include
from django.contrib.gis import admin
# from world.views import *
from djgeojson.views import GeoJSONLayerView
from pandas_test import views
# from world.models import WeatherStation
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^person/$', views.PersonList.as_view()),
    # url(r'^api/gis/country/(?P<position>[+-]?\d*.\d* [+-]?\d*.\d*)$', CountryQuery.as_view()),
    # url(r'^api/gis/station$', GeoJSONLayerView.as_view(model=WeatherStation, properties=('name', 'mrain'))),
    # url(r'^api/gis/inpoly/(?P<x>[+-]?\d*.\d*)/(?P<y>[+-]?\d*.\d*)$', InPoly),
    # url(r'^api/gis/station/(?P<position>[+-]?\d*.\d* [+-]?\d*.\d*)/(?P<dis>\d*.\d*)$', HcqStaQuery.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
