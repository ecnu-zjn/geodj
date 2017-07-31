# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.gis.db import models as gismodels
from django.db import models





class WorldBorder(gismodels.Model):
    # Regular Django fields corresponding to the attributes in the
    # world borders shapefile.
    name = models.CharField(max_length=50)
    area = models.IntegerField()
    pop2005 = models.IntegerField('Population 2005')
    fips = models.CharField('FIPS Code', max_length=2)
    iso2 = models.CharField('2 Digit ISO', max_length=2)
    iso3 = models.CharField('3 Digit ISO', max_length=3)
    un = models.IntegerField('United Nations Code')
    region = models.IntegerField('Region Code')
    subregion = models.IntegerField('Sub-Region Code')
    lon = models.FloatField()
    lat = models.FloatField()

    # GeoDjango-specific: a geometry field (MultiPolygonField), and
    # overriding the default manager with a GeoManager instance.
    mpoly = gismodels.MultiPolygonField()
    objects = gismodels.GeoManager()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.name


class WeatherStation(gismodels.Model):

    wmoid = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=256)
    prov = models.CharField(max_length=256)
    lon = models.FloatField()
    lat = models.FloatField()
    high = models.FloatField(null=True)
    mlowt = models.FloatField(null=True)
    std1 = models.IntegerField(null=True)
    hightsev = models.FloatField(null=True)
    std2 = models.IntegerField(null=True)
    hight = models.FloatField(null=True)
    lowt = models.FloatField(null=True)
    mrain =  models.FloatField(null=True)

    geom = gismodels.PointField()

    objects = gismodels.GeoManager()

    def __str__(self):
        return self.name