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