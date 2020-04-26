from django.urls import path
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('situation/',views.situation, name='situation'),
    path('add_person/',views.add_person, name='add_person'),
    path('statistics/',views.statistics, name='statistics'),
    path('login/',views.login, name='login'),
    path('reset_password',views.reset_password, name='reset_password')
]