from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView
from corona_app.models import reportes, comuna, region, activesCase, deathsporRegion, RRDate
from django.db.models import Avg, Max, Min, Sum, Count, Q

import csv
import urllib.request
from pip._vendor import requests
import json
from datetime import datetime
import numpy as np
import pandas as pd
import codecs
#Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from corona_app.serializers import ChartDataSerializer
from rest_framework.renderers import JSONRenderer

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView


# Create your views here.

def index(request):
    labels = []
    data = []

    query = reportes.objects.order_by('RDate')
    for rep in query:
        labels.append(rep.RDate)
        data.append(rep.RConfirmed)


    return render(request,'index.html',{
        'labels': labels,
        'data': data,
        })

def situation(request):
    return render(request,'profile.html',{})

def add_person(request):
    return render(request,'forms.html',{})

def statistics(request):
    return render(request,'tables.html',{})

def login(request):
    return render(request,'login.html',{})

def reset_password(request):
    return render(request,'reset-password.html',{})


# Create your views here.

class listAPI(ListView):
    model = comuna
    template_name = 'listAPI.html'

class comunasAPI(ListView):
    model = comuna
    template_name = 'comunas.html'

    def get_context_data(self, **kwargs):
        context = super(comunasAPI, self).get_context_data(**kwargs)
        url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv'
        ftpfile = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpfile, 'utf-8'))
        bandera = 0
        for column in csvfile:

            if bandera >0:
                 _, created = comuna.objects.get_or_create(
                Reg = region.objects.get(Codregion=column[1]),
                ComunaName = column[2],
                CodComuna = column[3],
                Poblation = column[4]
                )
            bandera = bandera + 1
        context = {}
        return context

class regionAPI(ListView):
    model = region
    template_name = 'region.html'

    def get_context_data(self, **kwargs):
        context = super(regionAPI, self).get_context_data(**kwargs)
        urlAPI = 'https://chile-coronapi.herokuapp.com/api/v3/models/regions'
        response = requests.get(urlAPI)
        if response.status_code == 200:
            response_json = response.json()
            for key in response_json:
                if int(key) < 10:
                    llave = '0'+key
                else:
                    llave = key
                _, created = region.objects.get_or_create(
                Codregion = llave,
                RegionName = response_json[key]['region'],
                Area = response_json[key]['area'],
                Lat = response_json[key]['lat'],
                Long = response_json[key]['long'],
                Population = response_json[key]['population']
                )
        context = {}
        return context


class activosAPI(ListView):
    model = activesCase
    template_name = 'actives.html'

    def get_context_data(self, **kwargs):
        context = super(activosAPI, self).get_context_data(**kwargs)
        url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto19/CasosActivosPorComuna.csv'

        ftpfile = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpfile, 'utf-8'))
        df = pd.DataFrame(csvfile)
        ancho = int(len(df.columns))
        largo = int(len(df))
        for i in range(5, ancho):
            for j in range(1, largo):
                if len(df[3][j]) is not 0:
                    if len(df[i][j]) is 0:
                        dato = 0
                    else:
                        dato = float(df[i][j])
                    _, created = activesCase.objects.get_or_create(
                    AcDate = df[i][0],
                    AcCod_comuna = comuna.objects.get(CodComuna=df[3][j]),
                    AcCantidad = dato
                    )


class deathsRegionAPI(ListView):
    model = deathsporRegion
    template_name = 'deathsRegion.html'

    def get_context_data(self, **kwargs):
        context = super(deathsRegionAPI, self).get_context_data(**kwargs)
        url = 'https://raw.githubusercontent.com/jorgeperezrojas/covid19-data/master/csv/muertes.csv'
        ftpfile = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpfile, 'utf-8'))
        df = pd.DataFrame(csvfile)
        ancho = int(len(df.columns))
        largo = int(len(df))

        for i in range(2, ancho):
            for j in range(1, largo):

                if len(df[i][j]) is 0:
                    dato = 0
                else:
                    dato = df[i][j]

                if len(df[0][j]) < 2:
                    reg = '0'+df[0][j]
                else:
                    reg = df[0][j]

                date = datetime.strptime(df[i][0] , '%m/%d/%Y').strftime('%Y-%m-%d')
                
                _, created = deathsporRegion.objects.get_or_create(
                DDate = date,
                DCodRegion = region.objects.get(Codregion=reg),
                Ddeaths = float(dato)
                )


class todosreportesAPI(ListView):
    model = reportes
    template_name = 'todosreportes.html'

    def get_context_data(self, **kwargs):
        context = super(todosreportesAPI, self).get_context_data(**kwargs)
        url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv'
        ftpfile = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpfile, 'utf-8'))
        df = pd.DataFrame(csvfile)
        ancho = int(len(df.columns)) - 1
        largo = int(len(df))

        for i in range(5, ancho):
            for j in range(1, largo):

                if len(df[i][j]) is 0:
                    dato = 0
                else:
                    dato = df[i][j]
                
                try:
                    actives = activesCase.objects.get(AcCod_comuna=df[3][j], AcDate = df[i][0]).AcCantidad
                except activesCase.DoesNotExist:
                    actives = float(0)

                try:
                    recovered = activesCase.objects.get(AcCod_comuna=df[3][j], AcDate = df[i][0]).AcCantidad - float(dato)
                except activesCase.DoesNotExist:
                    recovered = float(0)
                
                    
                _, created = RRDate.objects.get_or_create(
                # id = UuidCreate(),
                RDDate = df[i][0])

                _, created = reportes.objects.get_or_create(
                RDate = df[i][0],
                RComuna = comuna.objects.get(CodComuna=df[3][j]),
                RConfirmed = float(dato),
                RActive = float(actives),
                RRecovered = abs(recovered),
                #RDeath = 1,
                # RSymptomatic = 1,
                # RAsymptomatic = 1,
                #RTaza = 12
                )
    
        context = {}
        return context

class ChartDataViewSet(viewsets.ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = reportes.objects.all().order_by('RDate')
    serializer_class = ChartDataSerializer


class LineChartJSONView(BaseLineChartView):
    def get_labels(self):
        x_ax = []
        
        queryset = RRDate.objects.all().order_by('-RDDate')[:3]

        for i in reversed(queryset):
             x_ax.append(i.RDDate)
    
        return x_ax

    def get_providers(self):
        """Return names of datasets."""
        reg = []
        regiones = region.objects.all().order_by('Codregion')

        for k in regiones:
            reg.append(k.RegionName)
        #print(reg)
        return reg

    def get_data(self):
        """Return 3 datasets to plot."""
        dias = RRDate.objects.all().order_by('-RDDate')[:3]
        valores = []        
        for i in reversed(dias):
            queryset = reportes.objects.values('RComuna__Reg').filter(RDate = i.RDDate).annotate(Tot_Region=Sum('RConfirmed')).order_by('RComuna__Reg')
            valores.append(queryset)
        largo = int(len(valores))
        ancho = int(len(valores[1]))
        datos = np.arange((largo*ancho),dtype=np.int64).reshape(largo, ancho)
        for i in range(0,largo):
            cont = 0
            g = valores[i]
            for j in g:
                datos[i][cont] = j['Tot_Region']
                cont = cont + 1
        
        datos = datos.transpose()   
        return datos.tolist()


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()