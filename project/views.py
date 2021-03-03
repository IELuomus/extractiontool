
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import PageView
from django.core.files import File
from django.core.mail import send_mail
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import spacy
from spacy.symbols import nsubj, VERB
import tabula
import numpy as np
import pandas as pd
from django.http import HttpResponse
import os


def health(request):
    print('health check request')
    return HttpResponse(status=202)


def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        fs.save('templates_static/pdfs', uploaded_file)
        url = fs.url(name)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)

# def table_to_dataframe(request, template_name="table.html"):

def table_to_dataframe(request):
        file_path = "templates_static/pdfs/PURS_pdf.pdf"
        # files = []
        # for root, dirs, files in os.walk("media/"):
        #     for file in files:
        #         files.append(file)
        # print("files[0]: ", str(files))
        # uploaded_file = "media/%s"%(files[0])
        # print("path:", uploaded_file)
        # if uploaded_file:
        #     table = tabula.read_pdf(uploaded_file, pages="8", stream=True,  multiple_tables=True)
        # else:
        table = tabula.read_pdf(file_path, pages="8", stream=True,  multiple_tables=True)
        table = table[0].to_html() 
        return HttpResponse(table)

def parse(request):
    parse_result = {}
    if request.method == 'POST':
        nlp = spacy.load("en_core_web_trf")

        text=("Body size of Mustela africana averages larger than that "
        "of the other South American weasels, M. felipei (Colombian "
        "weasel) and M. frenata (long-tailed weasel—Hall 1951; Izor "
        "and de la Torre 1978), reaching about 500 mm in total "
        "length, versus 350 mm and 420 mm, respectively. M. "
        "africana exhibits a ventral stripe that is the same color as "
        "the dorsum (Fig. 1). M. felipei has a similar ventral marking "
        "but it is reduced to a spot on the chest or neck (Ram´ırezChaves et al. 2012) and M. frenata has no ventral markings. "
        "The tail is fairly long for a weasel ( 50% head-and-body "
        "length) and uniform in color. The soles of the feet lack fur "
        "and a thenar pad is present on forefoot (Hall 1951). The "
        "skull of M. africana (Fig. 2) has a mesopterygoid fossa "
        "reduced in comparison with M. felipei, and the auditory "
        "bullae are narrow, widely spaced, elongated, and less "
        "inflated than in M. frenata (Hall 1951; Izor and de la Torre "
        "1978; Abramow 2000). The nasals form an isosceles triangle, "
        "in contrast with M. felipei and M. frenata in which the "
        "lateral margins are subparallel anteriorly. The p2 is absent in "
        "M. africana (Izor and de la Torre 1978).")

        doc = nlp(text)

        noun_phrases=[chunk.text for chunk in doc.noun_chunks]
        verbs=[token.lemma_ for token in doc if token.pos_ == "VERB"]

        entities=[]

        for entity in doc.ents:
            entities.append(entity)
    
        parse_result = {'noun_phrases':noun_phrases, 'verbs':verbs, 'entities':entities}
    

    return render(request, 'parse.html', parse_result)
    


