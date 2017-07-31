### 1.添加源
```
sudo apt-get install  python-software-properties    
sudo apt-get install software-properties-common    
sudo add-apt-repository ppa:ubuntugis && sudo apt-get update
```

  
### 2.安装django和django-rest-framework

```
pip install Django==1.11.3
pip install djangorestframework
pip install markdown       
pip install django-filter
```


### 3.安装binutils、libpq-dev 、python-dev
```
sudo apt-get install binutils libpq-dev python-dev #后面的安装包可能依赖它
```


### 4.安装libproj-dev、libgeos-dev、gdal-bin、python-gdal
```
sudo apt-get install libproj-dev libgeos-dev gdal-bin python-gdal #安装gdal、proj4、geos等
```


### 5.安装postgresql-9.6
```
sudo add-apt-repository "deb http://apt.postgresql.org/pub/repos/apt/ precise-pgdg main"
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update    
sudo apt-get install postgresql-9.6
```
    
    

```
sudo apt-get install postgresql-9.6-postgis
```


```
#提示安装libgdal1，因此安装libgdal1,然后再安装postgresql-9.6
sudo apt-get install libgdal1    
sudo apt-get install postgresql-9.6-postgis
```


```
sudo apt-get install postgresql-server-dev-9.6
sudo pip install pip install psycopg2
```

### 6.postgres的数据库设置
#### 6.1 PostgreSQL数据库创建一个postgres用户作为数据库的管理员，密码随机，所以需要修改密码，方式如下：


```
步骤一：登录PostgreSQL
sudo -u postgres psql

步骤二：修改登录PostgreSQL密码
ALTER USER postgres WITH PASSWORD ‘postgres’;
注：密码postgres要用引号引起来
命令最后有分号

步骤三：退出PostgreSQL客户端
\q
```

#### 6.2 修改linux系统postgres用户的密码


```
PostgreSQL会创建一个默认的linux用户postgres，修改该用户密码的方法如下：

步骤一：删除用户postgres的密码

sudo passwd -d postgres
步骤二：设置用户postgres的密码

sudo -u postgres passwd
系统提示输入新的密码

Enter new UNIX password:
Retype new UNIX password:
passwd: password updated successfully
```
#### 6.3 创建空间数据库

```
sudo su - postgre

createdb geodjango

psql geodjango

CREATE EXTENSION postgis;

\q

exit
```
