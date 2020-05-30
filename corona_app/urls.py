from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views


urlpatterns = [
    path('',views.index, name='index'),
    path('situation/',views.situation, name='situation'),
    path('add_person/',login_required(views.add_person), name='add_person'),
    path('statistics/',views.statistics, name='statistics'),
    path('login_view/',views.login_view, name='login_view'),
    path('logout_view/',views.logout_view, name='logout_view'),
    path('reset_password',views.reset_password, name='reset_password'),
    path('questions/', views.questions, name='questions')
]