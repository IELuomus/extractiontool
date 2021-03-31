from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Pdf
from pdf_utility.pdf_reader import pdf_to_txt
import spacy
from spacy.symbols import nsubj, VERB
import en_core_web_lg
import json
from .forms import TraitValuesForm
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST, require_GET
from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.http import HttpResponse
import pandas as pd

current_pdf_id = []
def ajax_url(request):

    if request.method == 'POST':
   
        data = request.POST
        received_json_data=json.loads(request.body)
        jsondict = received_json_data['traitvalues']
        df = pd.DataFrame(list(jsondict.items()),columns = ['column1','column2'])
        lastrow = df.tail(1)
        print("START HERE!!!!SEE ME!!! -----------------------------------")
        # for index, row in lastrow.iterrows():
        #     sentence = row['column1']
        #     value = row['column2']
        print("lend(df)", len(df))
    
     
        lastrow = df.iloc[-1:]
        print(lastrow)
        print(lastrow["column1"])
        print(lastrow)
        print("OTHER PRINTS")
        train_data = []
        LABEL = "TRAITNAME"
        for key, value in received_json_data.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            for key, value in value.items():
                print("key:", str(key))
                print(" ")
                print("value: ", str(value))
                start = key.index(value)
                end = start + len(value)
                print("start and end:", start, end )
                train_instance = {"content" : key, "annotation" : [{
                    "label":["TRAITNAME"], 
                    "points" : [{"text" : value, "start" : start, "end" : end}]
                    }]
                }
                if train_instance not in train_data:         
                    train_data.append(json.dumps(train_instance))
                print("train_data", train_data)
        print("user.id: ", request.user.id)
        if current_pdf_id:
            print("pdf.id: ", current_pdf_id[0])

    return JsonResponse(data)


def parse(request, pk):
    parse_result = {}
    current_pdf_id.clear()
    current_pdf_id.append(pk)
    if request.method == 'POST':
        nlp = spacy.load("en_core_web_lg")
        
        pdf = Pdf.objects.get(pk=pk)
        file_path = pdf.pdf.path

        pdf_to_txt(pdf.pdf.name, file_path)

        with open(file_path+".txt", 'r', encoding="utf-8") as file:
            text = file.read().replace('\n', ' ')

        nlp.add_pipe("merge_entities")
        nlp.add_pipe("merge_noun_chunks")

        ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk(
            "./patterns_scientificNames.jsonl")

        doc = nlp(text)

        sentences_with_traits = []
        trait_words = ["weight",
                       "height",
                       "width",
                       "breadth",
                       "length",
                       "mass",
                       "body",
                       "tail",
                       "area",
                       "thickness",
                       "constriction",
                       "count",
                       "number",
                       "ratio",
                       "head-body",
                       "longevity",
                       "litter",
                       "size",
                       "range",
                       "index",
                       "ear",
                       "forearm"
                       ]

        for sentence in doc.sents:
            for trait in trait_words:
                if trait in sentence.text:
                    sentences_with_traits.append(sentence)
                    break

        # noun_phrases=[chunk.text for chunk in doc.noun_chunks]
        # verbs=[token.lemma_ for token in doc if token.pos_ == "VERB"]

        trait_text = ""
        for sent in sentences_with_traits:
            trait_text += sent.text

        # koesent = sentences_with_traits[0]

        # for token in koesent:
        #     print(token.text)

        trait_doc = nlp(trait_text)

        quantity_ner_labels = ["QUANTITY", "MONEY", "PERCENT", "CARDINAL"]
        scientificnames = [
            ent.text for ent in trait_doc.ents if ent.label_ == "SCIENTIFICNAME"]
        quantities = [
            ent.text for ent in trait_doc.ents if ent.label_ in quantity_ner_labels]
        # print(scientificnames)
        entities = []
        for entity in trait_doc.ents:
            entities.append(entity)
        number_of_sentences = len(sentences_with_traits)
        data = trait_doc.to_json()
        #data = json.dumps(sentences_with_traits)
        #print('data', data)
        parse_result = {'sentences': sentences_with_traits, 'entities': entities,
                        'scientificnames': scientificnames, 'quantities': quantities,
                        'number': number_of_sentences, 'data': data}
        #context['DJdata'] = json.dumps(DJdata)

    return render(request, 'parse.html', parse_result)
