from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from document.models import Pdf
from document.pdf_reader import pdf_to_txt
import spacy
#from spacy.symbols import nsubj, VERB
import en_core_web_lg
import json

from django.views.decorators.http import require_POST, require_GET
import re

current_pdf_id = []
@login_required
def parse(request, pk):
    parse_result = {}
    current_pdf_id.clear()
    current_pdf_id.append(pk)
    
    nlp = spacy.load("en_core_web_lg")

    pdf = Pdf.objects.get(pk=pk)
    file_path = pdf.filex.path

    pdf_to_txt(pdf.filex.name, file_path)

    with open(file_path+".txt", 'r', encoding="utf-8") as file:
        text = file.read().replace('\n', ' ')

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

    trait_text = ""
    for sent in sentences_with_traits:
        trait_text += sent.text

    nlp.add_pipe("merge_entities")
    nlp.add_pipe("merge_noun_chunks")

    ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk(
            "./patterns_scientificNames.jsonl")


    trait_doc = nlp(trait_text)
    sentences_with_ner_labels = []
    
    for sent in trait_doc.sents:
        sentence_with_labels = { 
                "content" : sent.text, 
                "annotation" : [                   
                ]
            }
        for ent in trait_doc.ents:           
            if (ent.sent.text == sent.text):           
                sentence_with_labels.get("annotation").append(
                    {
                        "label": [ent.label_],
                        "points": [
                            {
                                "text": ent.text, 
                                "start": ent.start_char-ent.sent.start_char, 
                                "end": ent.end_char-ent.sent.start_char}],
                    }
                )

        sentences_with_ner_labels.append(json.dumps(sentence_with_labels))

    quantity_ner_labels = ["QUANTITY", "MONEY", "PERCENT", "CARDINAL"]
    scientificnames = [
        ent.text for ent in trait_doc.ents if ent.label_ == "SCIENTIFICNAME"]
    quantities = [
        ent.text for ent in trait_doc.ents if ent.label_ in quantity_ner_labels]

    entities = []
    for entity in trait_doc.ents:
        entities.append(entity)
    
    parse_result = {
                    'json_sentences': sentences_with_ner_labels,
                    #'scientificnames': scientificnames, 
                    #'quantities': quantities
                    #'entities' : entities
                    }
        
    return render(request, 'parse.html', parse_result)
