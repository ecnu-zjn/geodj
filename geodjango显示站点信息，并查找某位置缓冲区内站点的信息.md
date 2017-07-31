### 新建数据库并设置数据库参数
由于导入数据时可能出现编码的问题，因此新建一个数据库mydb，并设置编码为UTF-8,其余操作不变。   
在setting中加入该数据库。

### 添加气象站点模型

```
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
```
### 进行migrate
略

### 导入数据
新建input.py进行数据的导入

数据格式为以\t分隔的csv，第一行为属性名称，编码类型为utf-8。

```
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
```
### 将数据输出为geojson格式

#### 安装django-geojson

安装django-geojson
```
pip install django-geojson
```

更新six
```
pip install six --upgrade
```

加入djgeojson

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'world',
    'rest_framework',
    'djgeojson',
]
```

在url中进行处理，增加以下内容

```
from djgeojson.views import GeoJSONLayerView
from world.models import WeatherStation

url(r'^api/gis/station$', GeoJSONLayerView.as_view(model=WeatherStation)),

```
### 结果
输入http://127.0.0.1:1234/api/gis/station    
 返回：
 
```
{"crs": {"type": "link", "properties": {"href": "http://spatialreference.org/ref/epsg/4326/", "type": "proj4"}}, "type": "FeatureCollection", "features": [{"geometry": {"type": "Point", "coordinates": [122.37, 53.47]}, "type": "Feature", "properties": {"model": "world.weatherstation"}, "id": 50136}, {"geometry": {"type": "Point", "coordinates": [124.72, 52.32]}, "type": "Feature", "properties": {"model": "world.weatherstation"}, "id": 50246}, {"geometry": {"type": "Point", "coordinates": [126.65, 51.72]}, "type": "Feature", "properties": {"model": "world.weatherstation"}, "id": 50353},   ......
```

### django框架如何输出geojson格式数据


```
from django.core.serializers import serialize
from world.models import WeatherStation

serialize('geojson', WeatherStation.objects.all(),
          geometry_field='point',
          fields=('name',))
```

### 输出缓冲区内的数据
#### 目的
场景：例如需要查询自己家附近5km以内的房价信息，就需要用到缓冲区。这里要做的是输入一个位置点，设置缓冲区距离，输出该缓冲区内的气象站点，并进一步计算相关信息，例如缓冲区内的平均年降水量。

#### 序列化

```
class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        # fields = ('name', 'mrain')
        fields = '__all__'
```

#### 编写视图，获取缓冲区数据

```
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
```

#### 添加路径

```
url(r'^api/gis/station/(?P<position>[+-]?\d*.\d* [+-]?\d*.\d*)/(?P<dis>\d*.\d*)$', HcqStaQuery.as_view()),
```

