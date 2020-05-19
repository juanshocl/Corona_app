from django.contrib.auth.models import User
from corona_app.models import reportes, comuna, region, activesCase, deathsporRegion
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class ChartDataSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = reportes
        fields = ['RDate', 'get_comuna', 'RConfirmed', 'RActive', 'RRecovered']

#'RComuna'