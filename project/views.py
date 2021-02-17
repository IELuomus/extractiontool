from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PageView
from django.core.mail import send_mail
from django.conf import settings

def homePageView(request):
    print('request')
    return render(request, "home.html")

def index(request):
    return render(request, 'index.html')

def myView(request):
    if request.user.is_authenticated:
        return render(request, 'index.html')
    else:
        return render(request, 'logout.html')

def health(request):
    print('health check request')
    return HttpResponse(status=202)

def email(request):
    subject = 'Thank you for registering to our site'
    message = ' it  means a world to us '
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['receiver@gmail.com',]
    send_mail( subject, message, email_from, recipient_list )
    return redirect('redirect to a new page')
