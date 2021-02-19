from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PageView
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def homePageView(request):
    print('request')
    return render(request, "home.html")

def index(request):
    return render(request, 'index.html')

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

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)