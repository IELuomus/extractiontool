
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PageView
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import tabula
from django.http import HttpResponse
import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.core.files.storage import default_storage
from .forms import PageNumberForm



current_file = []


def health(request):
    print('health check request')
    return HttpResponse(status=202)


@login_required
def upload(request):
    
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        current_file.append(name)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


@login_required
def table_to_dataframe(request):
    file_path = ""
    if not current_file:
        return HttpResponse("no pdf provided")
    file_path = "media/{}".format(current_file[0]) 
    if request.method == 'GET':
        page_number = request.GET.get('page_number', 1)
        table = tabula.read_pdf(file_path, pages=page_number, stream=True,  multiple_tables=True)
        table = table[0].to_html()
        return HttpResponse(table)
    else:
        return HttpResponse("no page number provided") 
