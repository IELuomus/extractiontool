from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Pdf
from .models import Json_Table
from django.contrib.sessions.models import Session
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
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.urls import reverse
from django_tables2 import MultiTableMixin, RequestConfig, SingleTableMixin, SingleTableView
from django_tables2.export.views import ExportMixin
from django_tables2.paginators import LazyPaginator

wanted_pdf = []
wanted_pdf_name = []
pdf_name = []
pdf_id = []




class TableListView(ListView):
    model = Json_Table
    template_name = 'selected_tables.html'

@login_required
def json_table_list(request, user_id, pdf_id):
    json_tables= JsonTable.objects.get(user_id=user_id, pdf_id=pdf_id)
    return render(request, 'selected_tables.html', {
        'tables': json_tables
    })
    

@login_required
def redirect_form(request, pk):
    
    context = {}
    pdf = Pdf.objects.get(pk=pk)
    file = pdf.pdf.path
    name = pdf.title
    pdf_id.clear()
    pdf_id.append(pk)
    pdf_name.clear()
    pdf_name.append(name)
    wanted_pdf.clear()
    wanted_pdf_name.clear()
    wanted_pdf.append(file)
    wanted_pdf_name.append(pdf. title)
    file_url = pdf.pdf.url
    context['url'] = file_url
    return render(request, 'redirect_form.html', context)


@login_required
def table_to_dataframe(request):
    context = {}
    user_id = request.user.id
    pdf_
    print(str(user))
    if not wanted_pdf:
        return HttpResponse("no pdf provided")

    file_path = wanted_pdf[0]
    file_name = pdf_name[0]
    page_number = request.GET.get('page_number')
    page = str(page_number)
    camelot_tables = camelot.read_pdf(file_path, flavor='stream', pages=page)
    camelot_tables.export("media/json/" +file_name + '_camelot.json', f='json')
    tables = tabula.read_pdf(file_path, pages=page_number, pandas_options={'header': None}, stream=True, multiple_tables=True)
    
    if camelot_tables:
 
        i=1
        for table in tables:
            table = pd.DataFrame(table)
            table.columns = table.iloc[0]
            table = table.reindex(table.index.drop(0)).reset_index(drop=True)
            table.columns.name = None
           
             #To write Excel
            # table.to_excel("media/" + current_file[0] + str(i)+'.xlsx', header=True, index=False)
            #To write CSV
            # table.to_csv("media/" + current_file[0] + str(i)+ '.csv', sep=',',header=True, 
            # index=False)

            table.to_json('media/json/' +file_name +'-page-' +page_number+ '-table-'+ str(i)+ '.json', orient='table', index=False)
         

            ROOT_FILE = 'media/json/' + file_name +'-page-' +page_number+ '-table-'+ str(i)+  '.json'
            json_data = open(ROOT_FILE)
            data = json.load(json_data)
            # for row in data:
            for key, value in data.items():
                js = Json_Table()
                js.user_id = request.user.id
                if pdf_id:
                    js.pdf_id = pdf_id[0]
                js.json_table = value
                js.save()
                
           
            table = table.to_html()
            text_file = open("templates/data" +str(i)+ ".html", "w", encoding='utf-8') 
            text_file.write(table) 
            i=i+1
        jobs = len(tables)   
        context['jobs'] = str(jobs)
        camelot_tables.export(file_path + '.json', f='json')
        return "%s?%s" % (redirect('selected_tables', args=(user_id= user_id, )),
                  urllib.urlencode(form.cleaned_data))
        # return TemplateResponse(request, 'table.html', context)
    else:
        return HttpResponse("no tables") 