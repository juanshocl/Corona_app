"""proyecto_corona URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from corona_app.views import listAPI, comunasAPI, regionAPI, todosreportesAPI, activosAPI, deathsRegionAPI, ChartDataViewSet, line_chart, line_chart_json
from rest_framework import routers, serializers


router = routers.DefaultRouter()
router.register('chardata', ChartDataViewSet)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('corona_app.urls')),
    path('datos/', listAPI.as_view(),name = 'listapi' ),
    path('comunas/', comunasAPI.as_view(),name = 'comunasapi' ),
    path('region/', regionAPI.as_view(),name = 'regionapi' ),
    path('activos/', activosAPI.as_view(),name = 'activosapi' ),
    path('muertes/', deathsRegionAPI.as_view(),name = 'muertesregionapi' ),
    #path('ultimosreportes/', ultimosreportesAPI.as_view(),name = 'ultimosreportesapi' ),
    path('todosreportes/', todosreportesAPI.as_view(),name = 'todosreportesapi' ),
    path('', include(router.urls)),
    #path('api/chart/data/', ChartDataViewSet.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json')
    

]
