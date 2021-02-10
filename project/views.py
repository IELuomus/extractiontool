from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PageView

def homePageView(request):
    print('request')
    return render(request, "home.html")

def catalogue(request):
    return render(request, "catalogue.html")


def index(request):
    return render(request, 'index.html')

def health(request):
    print('health check request')
    return HttpResponse(status=202)
