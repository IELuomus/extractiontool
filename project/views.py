from django.shortcuts import render
def homePageView(request):
    print('request')
    return render(request, "home.html")
def catalogue(request):
    return render(request, "catalogue.html")