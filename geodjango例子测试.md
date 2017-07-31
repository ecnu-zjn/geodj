## 1 创建项目

```
django-admin startproject geodj

cd geodj

python manage.py startapp world
```

## 2 查看测试数据的原始信息
```
mkdir world/data

cd world/data
wget http://thematicmapping.org/downloads/TM_WORLD_BORDERS-0.3.zip

unzip TM_WORLD_BORDERS-0.3.zip

cd ../..

 查看图层详细信息
 ogrinfo -so world/data/TM_WORLD_BORDERS-0.3.shp TM_WORLD_BORDERS-0.3
```

## 3 新建模型
```
from django.contrib.gis.db import models

class WorldBorder(models.Model):
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
    mpoly = models.MultiPolygonField()
    objects = models.GeoManager()

    # Returns the string representation of the model.
    def __str__(self):              # __unicode__ on Python 2
        return self.name
```

## 4 psycopg2更新

需要安装psycopg2 2.5.4版本以上，
```
pip install
psycopg2==2.5.4
```
## 5 生成数据表

```
python manage.py migrate
python manage.py migrate
```


## 6 利用shell进行测试


```
python manage.py shell
```

```
#利用图层的基本信息进行测试

import os
import world
world_shp=os.path.abspath(os.path.join(os.path.dirname(world.__file__),'data/TM_WORLD_BORDERS-0.3.shp'))

from django.contrib.gis.gdal import DataSource
ds = DataSource(world_shp)
print ds
#打印数据的图层数
print len(ds)
#获取第一层图层
lyr = ds[0]
print lyr
#获取图层几何类型
print lyr.geom_type
#获取要素数
print len(lyr)
#获取坐标
srs = lyr.srs
print srs
print srs.proj4
#获取图层字段信息及字段类型
print lyr.fields
[fld.__name__ for fld in lyr.field_types]
#打印各要素的点信息
for feat in lyr:
    print feat.get('NAME'), feat.geom.num_points
#获取具体要素的详细信息    
feat = lyr[234]
print feat.get('NAME')
geom = feat.geom
print geom.wkt
print geom.json
```
## 7 将图层的数据导入
#### 使用LayerMapping，在world的应用程序中创建一个load.py的文件
```
import os
from django.contrib.gis.utils import LayerMapping
from models import WorldBorder

world_mapping = {
    'fips' : 'FIPS',
    'iso2' : 'ISO2',
    'iso3' : 'ISO3',
    'un' : 'UN',
    'name' : 'NAME',
    'area' : 'AREA',
    'pop2005' : 'POP2005',
    'region' : 'REGION',
    'subregion' : 'SUBREGION',
    'lon' : 'LON',
    'lat' : 'LAT',
    'mpoly' : 'MULTIPOLYGON',
}

world_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), 'data/TM_WORLD_BORDERS-0.3.shp'))

def run(verbose=True):
    lm = LayerMapping(WorldBorder, world_shp, world_mapping,
                      transform=False, encoding='iso-8859-1')

    lm.save(strict=True, verbose=verbose)
```
#### 在shell中运行一下代码：
```
from world import load
load.run()
```
#### 也可以直接利用命令行生成模型和数据的映射
```
python manage.py ogrinspect world/data/TM_WORLD_BORDERS-0.3.shp WorldBorder \
    --srid=4326 --mapping --multi
```
#### 空间查询举例    
在包含特定点的WorldBorder表中找到国家/地区。
```
 pnt_wkt = 'POINT(-95.3385 29.7245)'
 
 from world.models import WorldBorder
qs = WorldBorder.objects.filter(mpoly__contains=pnt_wkt)
qs
```
当查询时，坐标不一致可自动转坐标
```
from django.contrib.gis.geos import Point, GEOSGeometry
pnt = Point(954158.1, 4215137.1, srid=32140)
qs = WorldBorder.objects.filter(mpoly__intersects=pnt)
qs
qs[0].mpoly.geojson
```
## 8 把数据放到地图上   
在admin.py中绑定WorldBorder模型
```
from django.contrib.gis import admin
from models import WorldBorder

admin.site.register(WorldBorder, admin.GeoModelAdmin)
```
在url中修改路径，加入空间数据管理的url

```
from django.conf.urls import url, include
from django.contrib.gis import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
]
```
创建管理员
```
python manage.py createsuperuser
python manage.py runserver
```
如果需要使用openstreetmap的底图进行展现，则可以将
```
admin.py中的admin.site.register(WorldBorder, admin.GeoModelAdmin)
```
修改为
```
admin.site.register(WorldBorder, admin.OSMGeoAdmin)
```
在[http://127.0.0.1:1234/admin/world/worldborder/](http://note.youdao.com/)可以对空间数据进行基本操作。

## 9 设计restful接口    

查询某个点在哪个国家内    

```
[get] api/gis/country/[position]
```


添加restfulframework模块及查询的接口地址,并且进行设置

```
#url.py
urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/gis/country/(?P<position>[+-]?\d*.\d* [+-]?\d*.\d*)$', CountryQuery.as_view()),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

```

```
#settings.py
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
]
```
将模型序列化
```
from rest_framework import serializers
from .models import WorldBorder

class WorldBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldBorder
        fields = ('name',)
```

返回查询到的国家
```
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from .models import WorldBorder
from .serializers import WorldBorderSerializer
from rest_framework.response import Response
from rest_framework import permissions

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
```
用以下url进行测试，http://127.0.0.1:1234/api/gis/country/-95.3385%2029.7245
```
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "name": "United States"
}
```



