from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from project.models import Pdf
from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from project.models import Pdf
from django.core.files import File
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import tabula
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
from .models import Json_Table, Trait_Table
from django.views.generic.list import ListView
from django.http import JsonResponse

wanted_pdf = []
wanted_pdf_name = []
pdf_name = []
pdf_ids = []


def post_url(request):

    LABEL = "TRAITNAME"
    if request.method == "POST":

        data = request.POST
        received_json_data = json.loads(request.body)
        species = received_json_data["species"]
        trait_name = received_json_data["trait_name"]
        trait_value = received_json_data["trait_value"]
        received_json_data["trait_unit"]
        trait_unit = received_json_data["trait_unit"]
        sex = received_json_data["sex"]
        print(species)
        print(trait_name)
        print(trait_value)
        print(trait_unit)
        print(sex)
        if wanted_pdf_name:
            source = wanted_pdf_name[0]
            print(source)
        if pdf_ids:
            print(pdf_ids[0])

        entry = Trait_Table()
        if pdf_ids:
            entry.pdf_id = pdf_ids[0]
        entry.scientific_name = species
        entry.sex = sex
        entry.trait_name = trait_name
        entry.trait_value = trait_value
        entry.trait_unit = trait_unit

        entry.save()

    return JsonResponse(data)


@login_required
def json_table_list(request, user_id, pdf_id, page_number):
    table_list = []
    data_frames = []

    json_tables = Json_Table.objects.filter(pdf_id=pdf_id).filter(
        page_number=page_number
    )
    data_f2 = []
    file_paths = []
    for table in json_tables:
        table_list.append(str(table.json_table))
        json_file_name = table.table
        json_field = json.dumps(table.json_table)
        data = pd.read_json(json_field)
        json_records = data.reset_index().to_json(orient="records")
        dataf = json.loads(json_records)
        if json_file_name not in file_paths:
            file_paths.append(str(json_file_name))

    i = 1
    data_f = []
    for entry in file_paths:
        file_path = "media/json/" + entry
        data = pd.read_json(file_path, orient="columns")
       
        data_frames.append(data)
        json_records = data.reset_index().to_json(orient="records")
        dataf = json.loads(json_records)
        data_f.append(dataf)
        json_data = dataf
        data_f2.append(json_data)

    i = i + 1
   
    return render(
        request,
        "selected_tables.html",
        {"d": data_f, "d2": json.dumps(data_f2), "n": n},
    )


@login_required
def redirect_form(request, pk):

    context = {}
    pdf = Pdf.objects.get(pk=pk)
    pdf_id = pdf.id
    file = pdf.pdf.path
    name = pdf.title
    pdf_ids.clear()
    pdf_ids.append(pdf_id)
    pdf_name.clear()
    pdf_name.append(name)
    wanted_pdf.clear()
    wanted_pdf_name.clear()
    wanted_pdf.append(file)
    wanted_pdf_name.append(pdf.title)
    file_url = pdf.pdf.url
    context["url"] = file_url
    return render(request, "redirect_form.html", context)


@login_required
def table_to_dataframe(request):
    context = {}
    user_id = request.user.id
    if pdf_ids:
        pdf_id = pdf_ids[0]
    if not wanted_pdf:
        return HttpResponse("no pdf provided")

    file_path = wanted_pdf[0]
    file_name = pdf_name[0]
    page_number = request.GET.get("page_number")
    page = str(page_number)
    camelot_tables = camelot.read_pdf(file_path, flavor="stream", pages=page)
    camelot_tables.export("media/json/" + file_name + ".json", f="json")
    # tables = tabula.read_pdf(
    #     file_path,
    #     pages=page_number,
    #     pandas_options={"header": None},
    #     stream=True,
    #     multiple_tables=True,
    # )

    if camelot_tables:

        i = 1
        for table in camelot_tables:
            # table = pd.DataFrame(table)'
            table = table.df
            table.columns = table.iloc[0]
            table = table.reindex(table.index.drop(0)).reset_index(drop=True)
            table.columns.name = None

            # To write Excel
            # table.to_excel("media/" + current_file[0] + str(i)+'.xlsx', header=True, index=False)
            # To write CSV
            # table.to_csv("media/" + current_file[0] + str(i)+ '.csv', sep=',',header=True,
            # index=False)

            # table.to_json('media/json/' + file_name + '-page-' + page_number +
            #               '-table-' + str(i) + '.json', orient='table', index=False)

            json_file_name = (
                file_name + "-page-" + page_number + "-table-" + str(i) + ".json"
            )

            ROOT_FILE = "media/json/" + json_file_name
            json_data = open(ROOT_FILE)
            data = json.load(json_data)
            # tables_exist = (
            #     Json_Table.objects.filter(pdf_id=pdf_id)
            #     .filter(page_number=page_number)
            #     .exists()
            # )
            tables_exist = (
                Json_Table.objects.filter(pdf_id=pdf_id)
                .filter(page_number=page_number)
                .filter(table_num=i)
                .exists()
            )
            print(tables_exist)

            if not tables_exist:
                js = Json_Table()
                js.user_id = request.user.id
                js.json_table = data
                if pdf_id:
                    js.pdf_id = pdf_id

                js.page_number = page_number
                js.table = json_file_name
                js.table_num = i
                js.save()
            else:
                pass
            i = i + 1
            # if not tables_exist:
            #     for key, value in data.items():
            #         js = Json_Table()
            #         js.user_id = request.user.id
            #         if pdf_id:
            #             js.pdf_id = pdf_id
            #         js.page_number = page_number
            #         js.json_table = value
            #         js.table = json_file_name
            #         js.save()
            # else:
            #     pass

            # table = table.to_html()
            # text_file = open("templates/data" + str(i) +
            #                  ".html", "w", encoding='utf-8')
            # text_file.write(table)

        # tables = Json_Table.objects.filter(pdf_id=pdf_id)

        return HttpResponseRedirect(
            reverse("selected_tables", args=(user_id, pdf_id, page_number))
        )
    else:
        return HttpResponse("no tables")
