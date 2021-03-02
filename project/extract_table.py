import tabula
import numpy as np
#the pd is the standard shorthand for pandas
import pandas as pd
from pandas import DataFrame
from django.http import HttpResponse
from django.shortcuts import render
from django.template.response import TemplateResponse
from django import forms
def table_to_dataframe(request, template_name="table.html"):
    file_path = "templates_static/pdfs/PURS_pdf.pdf"
    df = tabula.read_pdf(file_path, pages="8", stream=True, multiple_tables=True)
    print(len(df))
    args = {}
    html_format = to_html(df[0])
    args['table']= html_format
    # return HttpResponse(str(ready), content_type="text/plain")
    return TemplateResponse(request, template_name, args)

