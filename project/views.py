
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from .models import Pdf
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
from .forms import PageNumberForm, PdfForm
from document.pdf_reader import pdf_to_txt
import pandas as pd
import json
import spacy
from spacy.symbols import nsubj, VERB
import en_core_web_lg
import camelot

current_file = []


def health(request):
    print('health check request')
    return HttpResponse(status=202)


# @login_required
# def upload(request):
    
#     context = {}
#     if request.method == 'POST':
#         uploaded_file = request.FILES['document']
#         fs = FileSystemStorage()
#         name = fs.save(uploaded_file.name, uploaded_file)
#         file_path = "media/{}".format(name)
#         current_file.clear()
#         current_file.append(name)
#         pdf_to_txt(name, file_path)
#         context['url'] = fs.url(name)
#     return render(request, 'upload.html', context)

@login_required
def pdf_list(request):
    pdfs = Pdf.objects.all()
    return render(request, 'pdf_list.html', {
        'pdfs': pdfs
    })

@login_required
def upload_pdf(request):
    if request.method == 'POST':
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('pdf_list')
    else: 
        form = PdfForm()

    return render(request, 'upload_pdf.html', {
        'form': form
    })

def delete_pdf(request, pk):
    if request.method == 'POST':
        pdf = Pdf.objects.get(pk=pk)
        pdf.delete()
    return redirect('pdf_list')

