# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
from django.core.wsgi import get_wsgi_application

dev_work = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dev_work)

import geodj

os.environ['DJANGO_SETTINGS_MODULE'] = 'geodj.settings'
application = get_wsgi_application()

import csv
import json
from django.contrib.gis.geos import Point
from world.models import WeatherStation

def input():
    csv_file=os.path.abspath(os.path.join(os.path.dirname(__file__)))+'/data/Weatherstation.csv'
    with open(csv_file, 'rb') as f: 
        reader = csv.DictReader(f, delimiter='\t')
        for line in reader:
            print line
            prov = line.pop('prov')
            lon = float(line.pop('lon'))
            lat = float(line.pop('lat'))
            wmoid = int(line.pop('\xef\xbb\xbfwmoid'))
            name = line.pop('name')
            mrain = float(line.pop('mrain'))
            high = float(line.pop('high'))
            mlowt = float(line.pop('mlowt'))
            std1 = int(line.pop('std1'))
            hightsev = float(line.pop('hightsev'))
            std2 = int(line.pop('std2'))
            hight = float(line.pop('hight'))
            lowt = float(line.pop('lowt'))
            WeatherStation(wmoid=wmoid, name=name,lon=lon,lat=lat, geom=Point(lon, lat), prov = prov, mrain = mrain,
           high = high, mlowt = mlowt, std1 = std1, hightsev = hightsev, std2 = std2, hight = hight, lowt = lowt
           	).save()
if __name__ == '__main__':
	input()