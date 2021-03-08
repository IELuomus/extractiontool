
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
from django.template.response import TemplateResponse
import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.core.files.storage import default_storage
from .forms import PageNumberForm
from pdf_utility.pdf_reader import pdf_to_txt
import pandas as pd
import json
from pdf_utility.pdf_reader import pdf_to_txt

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
        
        file_path = "media/{}".format(name)
        pdf_to_txt(name, file_path)
        current_file.append(name)

        file_path = "media/{}".format(current_file[0])
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def name_of_the_file(request):
    return HttpResponse(current_file)


@login_required
def table_to_dataframe(request):
    file_path = ""
    if not current_file:
        return HttpResponse("no pdf provided")
    file_path = "media/{}".format(current_file[0]) 
    # if request.method == 'GET':
    page_number = request.GET.get('page_number')
    table = tabula.read_pdf(file_path, pages=page_number, stream=True, multiple_tables=True)
    if table:
        table = table[0].to_html()
        if table[1]:
            print("table[1]", str(table[1]))
            
        text_file = open("templates/data.html", "w") 
        text_file.write(table) 
        return TemplateResponse(request, 'table.html', {})
    else:
        return HttpResponse("no page number provided") 
