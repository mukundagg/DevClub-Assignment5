from django.shortcuts import render, redirect
from http.client import HTTPResponse
from django.http import *
from Users import models as user_models

def index(request):
    return redirect(f"/user/{request.user.entryNo}");#render(request, "index.html", {'allstudents': user_models.Student.objects.all(), 'allinstructors': user_models.Instructor.objects.all()});

def signin(request):
    if request.user.is_authenticated:
        return redirect("index/");
    else:
        return redirect("user/login/");