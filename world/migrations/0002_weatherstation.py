# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-18 07:02
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('world', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeatherStation',
            fields=[
                ('wmoid', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=256)),
                ('prov', models.CharField(max_length=256)),
                ('lon', models.FloatField()),
                ('lat', models.FloatField()),
                ('high', models.FloatField(null=True)),
                ('mlowt', models.FloatField(null=True)),
                ('std1', models.IntegerField(null=True)),
                ('hightsev', models.FloatField(null=True)),
                ('std2', models.IntegerField(null=True)),
                ('hight', models.FloatField(null=True)),
                ('lowt', models.FloatField(null=True)),
                ('mrain', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
    ]
