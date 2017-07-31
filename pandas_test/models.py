# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.
class Province(models.Model):
    name = models.CharField(max_length=10)
    def __unicode__(self):
        return self.name
 
class City(models.Model):
    name = models.CharField(max_length=5)
    province = models.ForeignKey(Province, related_name = "city")
    def __unicode__(self):
        return self.name
 
class Person(models.Model):
    firstname  = models.CharField(max_length=10)
    lastname   = models.CharField(max_length=10)
    visitation = models.ManyToManyField(City, related_name = "visitor")
    def __unicode__(self):
        return self.firstname + self.lastname