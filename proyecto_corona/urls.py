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
from corona_app.views import listAPI, comunasAPI, regionAPI, ultimosreportesAPI, todosreportesAPI, activosAPI, deathsRegionAPI

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('corona_app.urls')),
    path('datos/', listAPI.as_view(),name = 'listapi' ),
    path('comunas/', comunasAPI.as_view(),name = 'comunasapi' ),
    path('region/', regionAPI.as_view(),name = 'regionapi' ),
    path('activos/', activosAPI.as_view(),name = 'activosapi' ),
    path('muertes/', deathsRegionAPI.as_view(),name = 'muertesregionapi' ),
    path('ultimosreportes/', ultimosreportesAPI.as_view(),name = 'ultimosreportesapi' ),
    path('todosreportes/', todosreportesAPI.as_view(),name = 'todosreportesapi' ),
]
