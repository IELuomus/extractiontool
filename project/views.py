from django.shortcuts import render
from django.http import HttpResponse
from .models import PageView

def homePageView(request):
    print('request')
    return render(request, "home.html")
def catalogue(request):
    return render(request, "catalogue.html")
def health(request):
    """Takes an request as a parameter and gives the count of pageview objects as reponse"""
    return HttpResponse(PageView.objects.count())