from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from document.models import Pdf
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from project.models import TraitTable
from django.core.files import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.response import TemplateResponse
import os
from django.contrib.auth.decorators import login_required
from django.core.exceptions import *
from django.core.files.storage import default_storage
import pandas as pd
import json
import camelot
from django.contrib.sessions.models import Session
from django.contrib.auth.models import User
from django.views.generic import ListView
from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Json_Table
from django.views.generic.list import ListView
from django.http import JsonResponse

wanted_pdf = []
wanted_pdf_name = []
pdf_name = []
pdf_ids = []


def post_url(request):

    if request.method == "POST":

        data = request.POST
        received_json_data = json.loads(request.body)
        species = received_json_data["species"]
        trait_name = received_json_data["trait_name"]
        trait_value = received_json_data["trait_value"]
        received_json_data["trait_unit"]
        trait_unit = received_json_data["trait_unit"]
        sex = received_json_data["sex"]
        this_id = received_json_data["pk_"]
        print(species)
        print(trait_name)
        print(trait_value)
        print(trait_unit)
        print(sex)
        print(this_id)
        entry = TraitTable()
       
        p = Pdf.objects.get(id=this_id)
        entry.pdf_id = p
        entry.verbatimScientificName = species
        entry.sex = sex
        entry.verbatimTraitName = trait_name
        entry.verbatimTraitValue = trait_value
        entry.verbatimTraitUnit = trait_unit
        entry.save()

    return JsonResponse(data)


@login_required
def json_table_list(request, user_id, pdf_id, page_number):
    print("pdf_id: ", pdf_id)
    table_list = []
    data_frames = []

    json_tables = Json_Table.objects.filter(pdf_id=pdf_id).filter(
        page_number=page_number
    )

    file_paths = []
    for table in json_tables:
        table_list.append(str(table.json_table))
        json_file_name = table.table
        if json_file_name not in file_paths:
            file_paths.append(str(json_file_name))

    i = 1
    data_f1 = []
    data_f2 = []
    for entry in file_paths:
        file_path = "media/json/" + entry
        data = pd.read_json(file_path, orient="columns")
        data_frames.append(data)
        json_records = data.reset_index().to_json(orient="records")
        dataf = json.loads(json_records)
        data_f1.append(dataf)
        json_data = dataf
        data_f2.append(json_data)

    i = i + 1

    d2 = json.dumps(data_f2, ensure_ascii=False).encode("utf8")
    d2 = d2.decode()

    return render(
        request, "selected_tables.html", {"d": data_f1, "d2": d2, "pk": pdf_id}
    )


@login_required
def redirect_form(request, pk):
    context = {}
    pdf = Pdf.objects.get(pk=pk)
    # pdf_id = pdf.id
    # file = pdf.filex.path
    # name = pdf.title
    # pdf_ids.clear()
    # pdf_ids.append(pdf_id)
    # pdf_name.clear()
    # pdf_name.append(name)
    # wanted_pdf.clear()
    # wanted_pdf_name.clear()
    # wanted_pdf.append(file)
    # wanted_pdf_name.append(pdf.title)
    file_url = pdf.filex.url
    context["url"] = file_url
    context["pk"] = pk
    return render(request, "redirect_form.html", context)


@login_required
def table_to_dataframe(request):

    user_id = request.user.id
    pk_ = request.GET.get("pk")
    print("pk", pk_)

    # file_path = wanted_pdf[0]
    # file_name = pdf_name[0]
    pdf = Pdf.objects.get(pk=pk_)
    file_path = pdf.filex.path
    file_name = pdf.title
    page_number = request.GET.get("page_number")
    page = str(page_number)

    camelot_tables = camelot.read_pdf(file_path, flavor="stream", pages=page)
    os.makedirs("media/json/", exist_ok=True)
    camelot_tables.export("media/json/" + file_name + ".json", f="json")

    if camelot_tables:

        i = 1
        for table in camelot_tables:
            table = table.df
            table.columns = table.iloc[0]
            table = table.reindex(table.index.drop(0)).reset_index(drop=True)
            table.columns.name = None

            json_file_name = (
                file_name + "-page-" + page_number + "-table-" + str(i) + ".json"
            )

            ROOT_FILE = "media/json/" + json_file_name
            json_data = open(ROOT_FILE)
            data = json.load(json_data)

            tables_exist = (
                Json_Table.objects.filter(pdf_id=pk_)
                .filter(page_number=page_number)
                .filter(table_num=i)
                .exists()
            )
            print(tables_exist)

            if not tables_exist:
                js = Json_Table()
                js.user_id = request.user.id
                js.json_table = data
                js.pdf_id = pk_
                js.page_number = page_number
                js.table = json_file_name
                js.table_num = i
                js.save()
            else:
                pass
            i = i + 1
        return HttpResponseRedirect(
            reverse("selected_tables", args=(user_id, pk_, page_number))
        )
    else:
        return HttpResponse("no tables")
