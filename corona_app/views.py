from django.shortcuts import render
from django.template.context_processors import request

# Create your views here.

def index(request):
    return render(request,'index.html',{})

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