from django.shortcuts import render
import spacy
from spacy.symbols import nsubj, VERB
import en_core_web_sm


def parse(request):
    parse_result = {}
    if request.method == 'POST':
        nlp = spacy.load("en_core_web_sm")

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
