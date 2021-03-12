
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
from pdf_utility.pdf_sorter import is_text_pdf
import pandas as pd
import json
import spacy
from spacy.symbols import nsubj, VERB
import en_core_web_sm

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
        if is_text_pdf(name, file_path):
            pdf_to_txt(name, file_path) # run pdf_to_txt only on pdf's that contain text
        else:
            pass # edit this to run OCR here on image-only pdf's if that is what's wanted
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

def name_of_the_file(request):
    return HttpResponse(current_file[0])


@login_required
def table_to_dataframe(request):
    file_path = ""
    if not current_file:
        return HttpResponse("no pdf provided")
    file_path = "media/{}".format(current_file[0]) 
    # if request.method == 'GET':
    page_number = request.GET.get('page_number')
    tables = tabula.read_pdf(file_path, pages=page_number, stream=True, multiple_tables=True)
    if tables:
        # tables = tables[0].to_html()
        # text_file = open("templates/data.html", "w") 
        # text_file.write(tables) 
        # tables = tabula.read_pdf(file_path, pages=page_number, stream=True, multiple_tables=True, encoding='utf-8')

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

            table.to_json("media/" + current_file[0] + str(i)+ '.json', orient='table', index=False)
            table = table.to_html()
            text_file = open("templates/data" +str(i)+ ".html", "w") 
            text_file.write(table) 
            i=i+1
           
        return TemplateResponse(request, 'table.html', {'tables: ' : tables})
    else:
        return HttpResponse("no page number provided") 


def parse(request):
    parse_result = {}
    if request.method == 'POST':
        nlp = spacy.load("en_core_web_sm")

        # file_name = "testi2.pdf.txt"
        if not current_file:
            return HttpResponse("no pdf provided")
        file_name = current_file[0]+".txt"
        with open("media/{}".format(file_name), 'r', encoding="utf-8") as file:
            text = file.read().replace('\n', '')

        nlp.add_pipe("merge_entities")
        nlp.add_pipe("merge_noun_chunks")

        ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk("./patterns.jsonl")

        doc = nlp(text)

        noun_phrases=[chunk.text for chunk in doc.noun_chunks]
        verbs=[token.lemma_ for token in doc if token.pos_ == "VERB"]

        entities=[]

        for entity in doc.ents:
            entities.append(entity)
    
        parse_result = {'noun_phrases':noun_phrases, 'verbs':verbs, 'entities':entities}
    

    return render(request, 'parse.html', parse_result)

