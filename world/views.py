# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import WorldBorder, WeatherStation
from .serializers import WorldBorderSerializer, WeatherStationSerializer
from rest_framework.response import Response
from rest_framework import permissions
from django.http import HttpResponse
from django.contrib.gis.geos import Point, GEOSGeometry, Polygon
import os
import xlrd
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8') 

def InPoly(request,x,y):
    path=os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/data/polygon.xlsx'
    bk = xlrd.open_workbook(path)
    table = bk.sheets()[0] 
    nrows = table.nrows
    ncols = table.ncols
    plist=[]
    for i in range(1, nrows):
        plist.append(GEOSGeometry('POINT(%s %s)' %(table.cell(i,1).value, table.cell(i,2).value)))
    p = Polygon(plist)
    print p
    # pnt = Point(113.885, 22.517)
    lon=float(x)
    lat=float(y)
    pnt = Point(lon, lat)
    InOrNot=p.contains(pnt)
    # InOrNot=p.filter(poly__contains=pnt)
    Bldict={"InOrNot":InOrNot}
    print json.dumps(Bldict)
    return HttpResponse(json.dumps(Bldict), content_type="application/json")





class CountryQuery(APIView):
    def getCountryObj(self, position):
        print position
        #try:
        return WorldBorder.objects.filter(mpoly__contains=position)[0]
        #except:
            #raise Http404
    def get(self, request, position, format=None):
        position = 'POINT(' + position + ')'
        country = self.getCountryObj(position)
        return Response( WorldBorderSerializer(country).data )

class HcqStaQuery(APIView):
    def getCountryObj(self, position, dis):
        print position
        print dis
        print len(WeatherStation.objects.filter(geom__distance_lte = (position, dis)))
        #try:
        return WeatherStation.objects.filter(geom__distance_lte = (position, dis))
        # print hcq[0].mrain
    def get(self, request, position, dis, format=None):
        position = 'POINT(' + position + ')'
        station = self.getCountryObj(position, dis)
        return Response(WeatherStationSerializer(station, many=True).data )