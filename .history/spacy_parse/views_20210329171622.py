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
from django.http import JsonResponse
from django.http import HttpResponse


def ajax_url(request):

    print("fetch ")

    if request.method == 'POST':
        print("fetch")
        data = request.POST
        data_1 = json.dumps(r)
        data_1 = json.loads(data)
        data_1 = json.dumps(data_1)
        print(data_1)
        data_json = request.body
        data_json = json.dumps(data_json)
        data = json.loads(data_json)
        print(data_json)
        for key, value in data_1.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            print(key)
            print("value: ", str(value))

    return JsonResponse(data)


def parse(request, pk):
    parse_result = {}
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

        if request.method == 'GET':

            traitvalues = request.GET.get('traitvalues[]')
            traitvalues2 = request.GET.get('traitvalues')
            # arr = request.POST.get('traitvalues')
            print("traitvalues: ", str(traitvalues))
            print("traitvalues2: ", str(traitvalues2))

    return render(request, 'parse.html', parse_result)