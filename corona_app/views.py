from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import ListView
from corona_app.models import reportes, comuna, region, activesCase, deathsporRegion, RRDate
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Avg, Max, Min, Sum, Count
from django.views.defaults import page_not_found

import csv
import urllib.request
from pip._vendor import requests
import json
from datetime import datetime
import numpy as np
import pandas as pd
import codecs
# Rest Framework
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import permissions
from corona_app.serializers import ChartDataSerializer
from rest_framework.renderers import JSONRenderer

from django.views.generic import TemplateView
from chartjs.views.lines import BaseLineChartView




from corona_app.models import Noticias
# Create your views here.

def index(request):
    # Obtencion de datos desde la Base de datos.
    mostrar = True
    try:
        dia = RRDate.objects.all().order_by('-RDDate')[:3]

    except RRDate.DoesNotExist:
        mostrar = False

    if dia:
        try:
            diaanterior = int(reportes.objects.filter(RDate=dia[1].RDDate).aggregate(Sum('RConfirmed'))['RConfirmed__sum'])
        except reportes.DoesNotExist:
            mostrar = False
        try:
            dosAntes = int(reportes.objects.filter(RDate=dia[2].RDDate).aggregate(Sum('RConfirmed'))['RConfirmed__sum'])
        except reportes.DoesNotExist:
            mostrar = False
        try:
            Confirmados = int(reportes.objects.filter(RDate=dia[0].RDDate).aggregate(Sum('RConfirmed'))['RConfirmed__sum'])
        except reportes.DoesNotExist:
            mostrar = False

        try:
            ConfirmRepAnterior = int(reportes.objects.filter(RDate=dia[1].RDDate).aggregate(Sum('RConfirmed'))['RConfirmed__sum'])
        except reportes.DoesNotExist:
            mostrar = False

        try:
            Activos = int(reportes.objects.filter(RDate=dia[0].RDDate).aggregate(Sum('RActive'))['RActive__sum'])
        except reportes.DoesNotExist:
            mostrar = False

        try:
            ActivosRepAnterior = int(reportes.objects.filter(RDate=dia[1].RDDate).aggregate(Sum('RActive'))['RActive__sum'])
        except reportes.DoesNotExist:
            mostrar = False
        try:
            TotalFallecidosDiaAnterior = int(deathsporRegion.objects.filter(
                DDate=dia[1].RDDate).aggregate(Sum('Ddeaths'))['Ddeaths__sum'])
        except deathsporRegion.DoesNotExist:
            mostrar = False

        try:
            TotalFallecidos = int(deathsporRegion.objects.filter(
                DDate=dia[0].RDDate).aggregate(Sum('Ddeaths'))['Ddeaths__sum'])
        except deathsporRegion.DoesNotExist:
            mostrar = False
            
        Nuevos = Confirmados - diaanterior
        # Totales
        TotActives = Activos
        TotNuevos = Nuevos
        TotContagiados = Confirmados
        TotalRecuperados = Confirmados - Activos
        TotalRecuperadosRepAnterior = ConfirmRepAnterior - ActivosRepAnterior

        # Porcentajes
        PorActivoReport = float(((TotContagiados - diaanterior)*100)/diaanterior)
        PorCasoNuevo = float(((diaanterior - dosAntes)*100)/dosAntes)
        PorTotContagios = float((Confirmados - diaanterior)*100)/diaanterior
        PorTotFallecidos = float(
            ((TotalFallecidos - TotalFallecidosDiaAnterior)*100))/TotalFallecidosDiaAnterior
        PorTotRecuperados = float(
            ((TotalRecuperados - TotalRecuperadosRepAnterior)*100)/TotalRecuperadosRepAnterior)

            # Table, Trae los Top 10 del ultimo dia del reporte
        try:
            table = reportes.objects.filter(
                RDate=dia[0].RDDate).order_by('-RConfirmed')[:10]
        except reportes.DoesNotExist:
            mostrar = False
    else:
        mostrar = False

    if mostrar:
        return render(request, 'index.html',
            {
            'mostrar': mostrar,
            'activos': TotActives,
            'nuevos': TotNuevos,
            'contagiados': TotContagiados,
            'totfallecidos': TotalFallecidos,
            'totrecuperados': TotalRecuperados,
            'PorActivosIncre': PorActivoReport,
            'PorCasoNuevo': PorCasoNuevo,
            'PorTotCont': PorTotContagios,
            'PorTotFall': PorTotFallecidos,
            'PorTotReco': PorTotRecuperados,
            'tablas': table,
            })
    else:
        return render(request,'index.html',{
        'mostrar': False
        })


def situation(request):
    noticias = Noticias.objects.all()
    contexto = {'noticia': noticias}
    return render(request,'profile.html', contexto)

def add_person(request):
    status = 'NO_CONTENT'
    if request.method == 'POST':
        try:
            notice = Noticias()
            notice.titular = request.POST.get('txtTitular')
            notice.descripcion = request.POST.get('txtDescripcion')
            notice.fuente = request.POST.get('txtFuente')
            notice.save()
            status = 'OK'
        except :
            status = 'ERROR'
            print('ERROR EN EL INGRESO DE LA NOTICIA')
    return render(request,'forms.html',{'status':status})

def statistics(request):
    return render(request, 'tables.html', {})


def login_view(request):
    status = ''
    mensaje = ''
    if request.method == 'POST':
        username = request.POST.get('txtUsernameLogin')
        password = request.POST.get('txtPassLogin')
        user = authenticate(request, username=username, password=password)
        mensaje = user
        print(mensaje)
        if user:
            login(request, user)
            status = 'OK'
            return HttpResponseRedirect(reverse('index'))
        else:
            status = 'ERROR'
            messages.error(request, 'Error al iniciar sesión :c')
    variables = {'status': status,
                 'mensaje': mensaje}
    return render(request, 'login.html', variables)


@login_required(login_url='login_view')
def logout_view(request):
    logout(request)
    return(redirect('index'))


def reset_password(request):
    return render(request, 'reset-password.html', {})


# Create your views here.

class listAPI(ListView):
    model = comuna
    template_name = 'listAPI.html'


class comunasAPI(ListView):
    model = comuna
    template_name = 'comunas.html'

    # Datos de Consumiendo desde un archivo CSV
    model = comuna
    template_name = 'comunas.html'

    def get_context_data(self, **kwargs):
        context = super(comunasAPI, self).get_context_data(**kwargs)
        url = 'https://raw.githubusercontent.com/MinCiencia/Datos-COVID19/master/output/producto1/Covid-19.csv'
        ftpfile = urllib.request.urlopen(url)
        csvfile = csv.reader(codecs.iterdecode(ftpfile, 'utf-8'))
        bandera = 0
        for column in csvfile:

            if bandera > 0:
                _, created = comuna.objects.get_or_create(
                    Reg=region.objects.get(Codregion=column[1]),
                    ComunaName=column[2],
                    CodComuna=column[3],
                    Poblation=column[4]
                )
            bandera = bandera + 1

        context = {}
        return context


class regionAPI(ListView):
    # Datos de Region, Codigo, Nombre, Poblacion, Etc Desde una API.
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
                    Codregion=llave,
                    RegionName=response_json[key]['region'],
                    Area=response_json[key]['area'],
                    Lat=response_json[key]['lat'],
                    Long=response_json[key]['long'],
                    Population=response_json[key]['population']
                )
        context = {}
        return context


class activosAPI(ListView):
    # Casos activos por Comuna
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
                        AcDate=df[i][0],
                        AcCod_comuna=comuna.objects.get(CodComuna=df[3][j]),
                        AcCantidad=dato
                    )
        context = {}
        return context


class deathsRegionAPI(ListView):
    # Muertes Confirmadas por Region
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

                date = datetime.strptime(
                    df[i][0], '%m/%d/%Y').strftime('%Y-%m-%d')

                _, created = deathsporRegion.objects.get_or_create(
                    DDate=date,
                    DCodRegion=region.objects.get(Codregion=reg),
                    Ddeaths=float(dato)
                )
        context = {}
        return context


class todosreportesAPI(ListView):
    # Confirmados Incrementales
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
                    actives = activesCase.objects.get(
                        AcCod_comuna=df[3][j], AcDate=df[i][0]).AcCantidad
                except activesCase.DoesNotExist:
                    actives = float(0)

                try:
                    recovered = activesCase.objects.get(
                        AcCod_comuna=df[3][j], AcDate=df[i][0]).AcCantidad - float(dato)
                except activesCase.DoesNotExist:
                    recovered = float(0)

                _, created = RRDate.objects.get_or_create(
                    # id = UuidCreate(),
                    RDDate=df[i][0])

                _, created = reportes.objects.get_or_create(
                    RDate=df[i][0],
                    RComuna=comuna.objects.get(CodComuna=df[3][j]),
                    RConfirmed=float(dato),
                    RActive=float(actives),
                    RRecovered=abs(recovered),
                )

        context = {}
        return context


def questions(request):
    return render(request, 'questions.html', {})


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
        return reg

    def get_data(self):
        """Return 3 datasets to plot."""
        dias = RRDate.objects.all().order_by('-RDDate')[:3]
        valores = []
        for i in reversed(dias):
            queryset = reportes.objects.values('RComuna__Reg').filter(
                RDate=i.RDDate).annotate(Tot_Region=Sum('RConfirmed')).order_by('RComuna__Reg')
            valores.append(queryset)
        largo = int(len(valores))
        ancho = int(len(valores[1]))
        datos = np.arange((largo*ancho), dtype=np.int64).reshape(largo, ancho)
        for i in range(0, largo):
            cont = 0
            g = valores[i]
            for j in g:
                datos[i][cont] = j['Tot_Region']
                cont = cont + 1

        datos = datos.transpose()
        return datos.tolist()


line_chart = TemplateView.as_view(template_name='line_chart.html')
line_chart_json = LineChartJSONView.as_view()


class BarChartJSONView(BaseLineChartView):
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
        # print(reg)
        return reg

    def get_data(self):
        """Return 3 datasets to plot."""
        dias = RRDate.objects.all().order_by('-RDDate')[:3]
        valores = []
        for i in reversed(dias):
            queryset = deathsporRegion.objects.filter(
            DDate=i.RDDate).order_by('-DDate', 'DCodRegion')
            valores.append(queryset)

        largo = int(len(valores))
        ancho = int(len(valores[1]))
        datos = np.arange((largo*ancho), dtype=np.int64).reshape(largo, ancho)
        for i in range(0, largo):
            cont = 0
            g = valores[i]
            for j in g:
                datos[i][cont] = j.Ddeaths
                cont = cont + 1

        datos = datos.transpose()
        return datos.tolist()


line_chart2 = TemplateView.as_view(template_name='index.html')
line_chart_json2 = BarChartJSONView.as_view()


class PieChartJSONView(BaseLineChartView):
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
        # print(reg)
        return reg

    def get_data(self):
        """Return 3 datasets to plot."""
        dias = RRDate.objects.all().order_by('-RDDate')[:3]
        valores = []
        for i in reversed(dias):
            queryset = reportes.objects.values('RComuna__Reg').filter(
                RDate=i.RDDate).annotate(Tot_Region=Sum('RRecovered')).order_by('RComuna__Reg')
            valores.append(queryset)
        largo = int(len(valores))
        ancho = int(len(valores[1]))
        datos = np.arange((largo*ancho), dtype=np.int64).reshape(largo, ancho)
        for i in range(0, largo):
            cont = 0
            g = valores[i]
            for j in g:
                datos[i][cont] = j['Tot_Region']
                cont = cont + 1

        datos = datos.transpose()
        return datos.tolist()


line_chart3 = TemplateView.as_view(template_name='index.html')
line_chart_json3 = PieChartJSONView.as_view()


def mi_error_404(request, exception):
    return page_not_found(request, '404.html')
