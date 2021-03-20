from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Pdf
from pdf_utility.pdf_reader import pdf_to_txt
import spacy
from spacy.symbols import nsubj, VERB
import en_core_web_lg


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

        ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk("./patterns_scientificNames.jsonl")

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

        trait_doc = nlp(trait_text)
        
        entities=[]

        for entity in trait_doc.ents:
            entities.append(entity)

        parse_result = {'sentences': sentences_with_traits, 'entities':entities}

    return render(request, 'parse.html', parse_result)
