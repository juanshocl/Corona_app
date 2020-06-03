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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('corona_app.urls')),
    # path('datos/', login_required(listAPI.as_view()),name = 'listapi' ),
    # path('comunas/', login_required(comunasAPI.as_view()),name = 'comunasapi' ),
    # path('region/', login_required(regionAPI.as_view()),name = 'regionapi' ),
    # path('activos/', login_required(activosAPI.as_view()),name = 'activosapi' ),
    # path('muertes/', login_required(deathsRegionAPI.as_view()),name = 'muertesregionapi' ),
    # path('todosreportes/', login_required(todosreportesAPI.as_view()),name = 'todosreportesapi' ),
    #path('', include(router.urls)), 
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('chart', line_chart, name='line_chart'),
    # path('chartJSON', line_chart_json, name='line_chart_json'),
    # path('chart2', line_chart2, name='line_chart'),
    # path('chartJSON2', line_chart_json2, name='line_chart_json2'),
    # path('chart3', line_chart3, name='line_chart'),
    # path('chartJSON3', line_chart_json3, name='line_chart_json3'),
    # path('cargardatos', cargardatos, name='cargardatos'),

]
