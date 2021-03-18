from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Pdf
from pdf_utility.pdf_reader import pdf_to_txt

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from project.models import Pdf
from django.core.files import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import tabula
from django.http import HttpResponse
from django.template.response import TemplateResponse
import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.core.files.storage import default_storage
import pandas as pd
import json
import camelot

@login_required
def table_to_dataframe(request, pk):
    context = {}
    # file_path = ""
    # if not current_file:
    #     return HttpResponse("no pdf provided")
    # file_path = "media/{}".format(current_file[0]) 
    pdf = Pdf.objects.get(pk=pk)
    file_path = pdf.pdf.path

    page_number = 8 #request.GET.get('page_number')
   
    camelot_tables = camelot.read_pdf(file_path, flavor='stream', pages='all')
    camelot_tables.export(file_path + '.json', f='json')
    tables = tabula.read_pdf(file_path, pages='all', pandas_options={'header': None}, stream=True, multiple_tables=True)
    if tables:
 
        i=1
        for table in tables:
            table.columns = table.iloc[0]
            table = table.reindex(table.index.drop(0)).reset_index(drop=True)
            table.columns.name = None
             #To write Excel
            # table.to_excel("media/" + current_file[0] + str(i)+'.xlsx', header=True, index=False)
            #To write CSV
            # table.to_csv("media/" + current_file[0] + str(i)+ '.csv', sep=',',header=True, 
            # index=False)

            table.to_json(file_path + str(i)+ '.json', orient='table', index=False)
            table = table.to_html()
            text_file = open("templates/data" +str(i)+ ".html", "w") 
            text_file.write(table) 
            i=i+1
        jobs = len(tables)   
        context['jobs'] = str(jobs)
        return TemplateResponse(request, 'table.html', context)
    else:
        return HttpResponse("no tables") 
