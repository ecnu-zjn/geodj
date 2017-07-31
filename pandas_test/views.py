# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from pandas_test.models import Person
from django_pandas.io import read_frame
import json
# Create your views here.
class  PersonList(APIView):
    """
    List all snippets, or create a new snippet.
    """
    def get(self, request, format=None):
        persons = Person.objects.all()
        person_df=read_frame(persons,index_col='id')
        person_js=person_df.to_json(orient="records")
        p=json.loads(person_js)
        return Response(p)