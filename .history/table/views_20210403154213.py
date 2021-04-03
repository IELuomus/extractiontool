from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Pdf

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
from django.http import HttpResponseRedirect
from .models import Json_Table
from django.views.generic.list import ListView
wanted_pdf = []
wanted_pdf_name = []
pdf_name = []
pdf_ids = []


#    products = Product.objects.filter(**filters)
#     return render(request, 'products.html', {'products': products})
class TableListView(ListView):

    
    model = Json_Table
    paginate_by = 100  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

# obj, created = Person.objects.filter(
#     Q(first_name='Bob') | Q(first_name='Robert'),
# ).get_or_create(last_name='Marley', defaults={'first_name': 'Bob'})

@login_required
def json_table_list(request, user_id, pdf_id):
    table_list = []
    pdf_id = pdf_ids[0]
    json_tables= Json_Table.objects.filter(pdf_id=pdf_id)
    
    for table in json_tables:
        # print(str(table.json_table))
        table_list.append(str(table.json_table))
    return render(request, 'selected_tables.html', {'object_list': json_tables, 'table_list': table_list})

@login_required
def redirect_form(request, pk):
    
    context = {}
    pdf = Pdf.objects.get(pk=pk)
    pdf_id = pdf.id
    file = pdf.pdf.path
    name = pdf.title
    pdf_ids.clear()
    pdf_ids.append(pdf_id)
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
    if pdf_ids:
        pdf_id = pdf_ids[0]
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
            if not Json_Table.objects.filter(pdf_id=pdf_id).exists():
                for key, value in data.items():
                    js = Json_Table()
                    js.user_id = request.user.id
                    if pdf_id:
                        js.pdf_id = pdf_id
                    js.page_number = page_number
                    js.json_table = value
                    js.save()
            else:
                pass
                
           
            table = table.to_html()
            text_file = open("templates/data" +str(i)+ ".html", "w", encoding='utf-8') 
            text_file.write(table) 
            i=i+1
        jobs = len(tables)   
        context['jobs'] = str(jobs)
        camelot_tables.export(file_path + '.json', f='json')
        tables  = Json_Table.objects.filter(pdf_id=pdf_id)
     
        return HttpResponseRedirect(reverse('selected_tables', args=(user_id, pdf_id, p )))
     
        # return TemplateResponse(request, 'table.html', context)
    else:
        return HttpResponse("no tables") 