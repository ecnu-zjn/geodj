
## geodjango模块在webgis中的应用
### 1.项目简介
项目主要应用django的geodjango模块及postgres数据库的空间数据扩展模块，对今后其它项目中的gis功能做基础储备。

### 2.涉及的软件及扩展包
- django（包含geodjango）
- postgres及postgis
- geos扩展
- gdal扩展
- proj4扩展
- django-rest-framework

### 3.已测试的功能
##### 1.查询某个未知点在哪个国家
在url中输入相应的经纬度，以restful的规范进行处理，返回json格式的国家信息。其中国家信息添加到admin的管理平台上，可进行数据的各类基本操作。

##### 2.判断某个点是否在某个多边形区域内部
从包含多边形边界点的excel表中读取点数据，形成一个多边形对象，判断点是否在多边形内部，返回结果为json数据，含true则在内部，反之在外部。



## pandas模块在在django-restful-framework中的使用

## 1.项目简介

主要尝试在django-restful-framework中使用pandas，以便在数据处理、统计功能比较复杂时能够快速解决问题。

## 2.使用过程

2.1 新建pandas-test应用

`python manage.py createapp pandas-test`

2.2 引入django-pandas

```
pip install django-pandas

INSTALLED_APPS = [
    'django.contrib.admin',
      ......
    'pandas_test',
    'django_pandas'
]
```

2.3 数据库连接略

2.4 模型

    # -*- coding: utf-8 -*-
    from __future__ import unicode_literals
    from django.db import models
    
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
2.5 视图的做法

    -- coding: utf-8 --

    from future import unicode_literals

    from django.shortcuts import render

    from rest_framework.views import APIView

    from rest_framework.response import Response

    from rest_framework import status

    from pandas_test.models import Person

    from django_pandas.io import read_frame

    import json

    class  PersonList(APIView):
        def get(self, request, format=None):
            persons = Person.objects.all()
            person_df=read_frame(persons,index_col='id') 转为dataframe格式的数据
            person_js=person_df.to_json(orient="records") 转为json格式的数据
            p=json.loads(person_js) json转为对象
            return Response(p)`