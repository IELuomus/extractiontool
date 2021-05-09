from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import json
#from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST, require_GET
from .models import TraitnameLearnData
from django.http import JsonResponse
#from django.http import HttpResponse


current_pdf_id = []
train_data = []

def fetch_url(request):

    LABEL = "TRAITNAME"
    if request.method == "POST":

        data = request.POST

        train_instance = json.loads(request.body)
        #print("received:", train_instance)

        TraitnameLearnData.objects.create(data=train_instance)

    print("user.id: ", request.user.id)
    if current_pdf_id:
        print("pdf.id: ", current_pdf_id[0])

    return JsonResponse(data)
