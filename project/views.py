
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
from pdf_utility.pdf_reader import pdf_to_txt
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


@login_required
def upload(request):
    
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        file_path = "media/{}".format(name)
        current_file.clear()
        current_file.append(name)
        pdf_to_txt(name, file_path)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

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

def name_of_the_file(request):
    return HttpResponse(current_file[0])

# @login_required
# def table_to_dataframe(request, pk):
#     context = {}
#     # file_path = ""
#     # if not current_file:
#     #     return HttpResponse("no pdf provided")
#     # file_path = "media/{}".format(current_file[0]) 
#     pdf = Pdf.objects.get(pk=pk)
#     file_path = pdf.pdf.path

#     page_number = 8 #request.GET.get('page_number')
   
#     camelot_tables = camelot.read_pdf(file_path, flavor='stream', pages='all')
#     camelot_tables.export(file_path + '.json', f='json')
#     tables = tabula.read_pdf(file_path, pages='all', pandas_options={'header': None}, stream=True, multiple_tables=True)
#     if tables:
 
#         i=1
#         for table in tables:
#             table.columns = table.iloc[0]
#             table = table.reindex(table.index.drop(0)).reset_index(drop=True)
#             table.columns.name = None
#              #To write Excel
#             # table.to_excel("media/" + current_file[0] + str(i)+'.xlsx', header=True, index=False)
#             #To write CSV
#             # table.to_csv("media/" + current_file[0] + str(i)+ '.csv', sep=',',header=True, 
#             # index=False)

#             table.to_json(file_path + str(i)+ '.json', orient='table', index=False)
#             table = table.to_html()
#             text_file = open("templates/data" +str(i)+ ".html", "w") 
#             text_file.write(table) 
#             i=i+1
#         jobs = len(tables)   
#         context['jobs'] = str(jobs)
#         return TemplateResponse(request, 'table.html', context)
#     else:
#         return HttpResponse("no page number provided") 


# def parse(request, pk):
#     parse_result = {}
#     if request.method == 'POST':
#         nlp = spacy.load("en_core_web_lg")

#         # if not current_file:
#         #     return HttpResponse("no pdf provided")
#         pdf = Pdf.objects.get(pk=pk)
#         file_path = pdf.pdf.path

#         pdf_to_txt(pdf.pdf.name, file_path)
#         # file_name = current_file[0]+".txt"
#         # file_name_new = Pdf.objects.get(title="uusi")
#         with open(file_path+".txt", 'r', encoding="utf-8") as file:
#             text = file.read().replace('\n', ' ')


#         nlp.add_pipe("merge_entities")
#         nlp.add_pipe("merge_noun_chunks")

#         ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk("./patterns_scientificNames.jsonl")

#         doc = nlp(text)

#         sentences_with_traits = []
#         trait_words = ["weight", 
#         "height",
#         "width",
#         "breadth",
#         "length",
#         "mass",
#         "body",
#         "tail",
#         "area",
#         "thickness",
#         "constriction", 
#         "count",
#         "number",
#         "ratio",
#         "head-body",
#         "longevity",
#         "litter",
#         "size",
#         "range",
#         "index",
#         "ear",
#         "forearm"
#         ]

#         for sentence in doc.sents:
#             for trait in trait_words:
#                 if trait in sentence.text:
#                     sentences_with_traits.append(sentence)
#                     break
        
#         # noun_phrases=[chunk.text for chunk in doc.noun_chunks]
#         # verbs=[token.lemma_ for token in doc if token.pos_ == "VERB"]

#         trait_text = ""
#         for sent in sentences_with_traits:
#             trait_text += sent.text

#         trait_doc = nlp(trait_text)
        
#         entities=[]

#         for entity in trait_doc.ents:
#             entities.append(entity)

#         parse_result = {'sentences': sentences_with_traits, 'entities':entities}

#     return render(request, 'parse.html', parse_result)

<<<<<<< HEAD
@login_required
def table_to_dataframe(request):
    file_path = ""
    if not current_file:
        return HttpResponse("no pdf provided")
    file_path = "media/{}".format(current_file[0]) 
    if request.method == 'GET':
        page_number = request.GET.get('page_number', 1)
        table = tabula.read_pdf(file_path, pages=page_number, stream=True,  multiple_tables=False)
        table = table[0].to_html()
        return HttpResponse(table)
    else:
        return HttpResponse("no page number provided") 
=======
>>>>>>> main
