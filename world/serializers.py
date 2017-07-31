from rest_framework import serializers
from .models import WorldBorder, WeatherStation

class WorldBorderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorldBorder
        fields = ('name',)

class WeatherStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeatherStation
        # fields = ('name', 'mrain')
        fields = '__all__'