
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PageView
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import spacy
from spacy.symbols import nsubj, VERB
import en_core_web_sm

def health(request):
    print('health check request')
    return HttpResponse(status=202)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

    