from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
from spacy_parse.forms import TraitValuesForm
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST, require_GET
#from django.contrib.sessions.models import Session
from django.http import JsonResponse
from django.http import HttpResponse


current_pdf_id = []
train_data = []

def fetch_url(request):

        LABEL = "TRAITNAME"
        if request.method == 'POST':

            data = request.POST
            received_json_data = json.loads(request.body)
            sentence = received_json_data['sentence']
            trait_name = received_json_data['trait_name']
            print(sentence)
            print(trait_name)
      
            start = sentence.find(trait_value)
            print("start: ", str(start))
            end = start + len(trait_value)
            print("start and end:", start, end)
            train_instance = {"content": sentence, "annotation": [{
            "label": ["TRAITNAME"],
            "points": [{"text": trait_value, "start": start, "end": end}]
            }]}
            if train_instance not in train_data:
                train_data.append(json.dumps(train_instance))
        print("train_data list below: ")
        print(*train_data, sep="\n")

        print("user.id: ", request.user.id)
        if current_pdf_id:
            print("pdf.id: ", current_pdf_id[0])

        return JsonResponse(data)
