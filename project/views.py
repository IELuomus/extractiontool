from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse

# from .models import Pdf
from document.models import Pdf
from .models import TraitTable
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
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
import sys
import platform
from django.http import JsonResponse
from django.core import serializers

current_file = []


def health(request):
    print("health check request")
    return HttpResponse(status=202)



@login_required
def pdf_list(request):
    # get only own pdfs
    sql = f"SELECT * from doc_pdf WHERE id IN (SELECT document_id FROM doc_owner WHERE owner_id = {request.user.id})"
    pdfs = Pdf.objects.raw(sql)

    return render(request, "pdf_list.html", {"pdfs": pdfs})


@login_required
def upload_pdf(request):
    if request.method == "POST":
        form = PdfForm(request.POST, request.FILES)
        if form.is_valid():
            pdf = form.save(commit=False)
            pdf.user = request.user
            pdf.save()
            try:
                if (pdf.new_file_upload == 'true'):
                    # start django-q tasks
                    print(f'operating system recognized as {sys.platform}')
                    print(f'processor recognized as {platform.processor()}')
                    if sys.platform == "darwin":
                        # @ macOS
                        print("runnig in macOS")
                        print("skipping set_up_document_background_image_tasks(pdf)")
                    elif sys.platform == "win32":
                        # @ Windows
                        print("runnig in Windows")
                        print("skipping set_up_document_background_image_tasks(pdf)")
                    else:
                        # default (linux)
                        from tesserakti.tessera_util import set_up_document_background_image_tasks
                        set_up_document_background_image_tasks(pdf)
            except AttributeError:
                print(f'pdf with id {pdf.id} was NOT new. not calling document tasks.')

            return redirect("pdf_list")
    else:
        form = PdfForm()

    return render(request, "upload_pdf.html", {"form": form})


def delete_pdf(request, pk):
    if request.method == "POST":
        pdf = Pdf.objects.get(pk=pk)
        pdf.user = request.user
        pdf.delete()
    return redirect("pdf_list")

@login_required
def search_data(request):
    if request.method == "GET":
        return render(request, "search.html")
    else:
        json_data = json.loads(request.body)
        sn = json_data["scientific_name"]
        results = TraitTable.objects.filter(verbatimScientificName__icontains=sn)
        res_json = serializers.serialize('json', results)
        return HttpResponse(res_json, content_type='application/json')  
