from django.urls import path, include
from . import views
from corona_app.views import listAPI, comunasAPI, regionAPI, todosreportesAPI, activosAPI, deathsRegionAPI, ChartDataViewSet, line_chart, line_chart_json, line_chart_json2, line_chart_json3, line_chart2, line_chart3, mi_error_404

from rest_framework import routers, serializers
from django.contrib.auth.decorators import login_required

router = routers.DefaultRouter()
router.register('chardata', ChartDataViewSet)


router = routers.DefaultRouter()
router.register('chardata', ChartDataViewSet)
from django.conf.urls import handler404
from django.contrib.auth.decorators import login_required

handler404 = mi_error_404


urlpatterns = [
    path('',views.index, name='index'),
    path('situation/',views.situation, name='situation'),
    path('add_person/',login_required(views.add_person), name='add_person'),
    path('statistics/',views.statistics, name='statistics'),
    path('login_view/',views.login_view, name='login_view'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('reset_password',views.reset_password, name='reset_password'),
    path('questions/', views.questions, name='questions'),
    path('datos/', login_required(listAPI.as_view()),name = 'listapi' ),
    path('comunas/', login_required(comunasAPI.as_view()),name = 'comunasapi' ),
    path('region/', login_required(regionAPI.as_view()),name = 'regionapi' ),
    path('activos/', login_required(activosAPI.as_view()),name = 'activosapi' ),
    path('muertes/', login_required(deathsRegionAPI.as_view()),name = 'muertesregionapi' ),
    path('todosreportes/', login_required(todosreportesAPI.as_view()),name = 'todosreportesapi' ),
    path('', include(router.urls)), 
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('chart', line_chart, name='line_chart'),
    path('chartJSON', line_chart_json, name='line_chart_json'),
    path('chart2', line_chart2, name='line_chart'),
    path('chartJSON2', line_chart_json2, name='line_chart_json2'),
    path('chart3', line_chart3, name='line_chart'),
    path('chartJSON3', line_chart_json3, name='line_chart_json3'),
]