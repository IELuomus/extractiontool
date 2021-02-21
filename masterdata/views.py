# from cradle_of_mankind.decorators import remember_last_query_params
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from project import settings
from csv import DictReader
import os
from django.contrib import messages
from masterdata.forms import SourceDataImportForm
from users.views import user_is_data_admin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import redirect, render
from masterdata.models import Source, SourceData, SourceEntity, SourceField, SourceValue


# @login_required
# @user_passes_test(user_is_data_admin)
# @remember_last_query_params('source-list', ['page', 'source'])
# def source_list(request):
#     sources = Source.objects.all()
#     source = get_source(request)
#     source_fields = SourceField.objects.filter(source=source)
#     source_entitites = get_source_entities(request, source)
#     source_entity_data = get_source_entity_data(
#         source_entitites, source_fields)
#     return render(request, 'masterdata/source_list.html',
#                   {'selected_source': source,
#                    'sources': sources,
#                    'source_fields': source_fields,
#                    'source_entity_data': source_entity_data,
#                    'page_obj': source_entitites})


# def get_source_entity_data(entities, fields):
#     data = {}
#     for entity in entities:
#         entity_data = []
#         for field in fields:
#             value = SourceData.objects.filter(
#                 source_entity=entity, source_field=field).first().source_value.value
#             entity_data.append(value)
#         data[entity] = entity_data
#     return data


# def get_source(request):
#     source_id = request.GET.get('source')
#     if source_id:
#         source = Source.objects.get(pk=source_id)
#     else:
#         source = Source.objects.all().first()
#     return source


# def get_source_entities(request, source):
#     source_entities = SourceEntity.objects.filter(source=source)
#     page = request.GET.get('page', 1)
#     paginator = Paginator(source_entities, 15)
#     try:
#         page_entities = paginator.page(page)
#     except PageNotAnInteger:
#         page_entities = paginator.page(1)
#     except EmptyPage:
#         page_entities = paginator.page(paginator.num_pages)
#     return page_entities


# @login_required
# @user_passes_test(user_is_data_admin)
# def import_data(request):
#     if request.method == 'POST':
#         form = SourceDataImportForm(request.POST, request.FILES)
#         if form.is_valid():
#             source_name = request.POST['source_name']
#             f = request.FILES['file']
#             save_uploaded_file(f)
#             save_data(source_name, f)
#             messages.success(request, "Import was succesful!")
#             redirect('index')
#     form = SourceDataImportForm()
#     return render(request, 'masterdata/import_source_data.html', {'form': form})


# def save_data(source_name, file):
#     with open(os.path.join(settings.MEDIA_ROOT, 'masterdata', file.name), encoding='utf8') as f:
#         try:
#             source = Source.objects.get(name=source_name)
#         except Source.DoesNotExist:
#             source = Source()
#             source.name = source_name
#             source.save()

#         data = DictReader(f)
#         rows = 0
#         for row in data:
#             rows += 1
#         print(rows)
#         f.seek(0)
#         data = DictReader(f)
#         print(f"Processing... ({rows} rows)")
#         for index, row in enumerate(data, 1):
#             print_progress(index, rows)

#             source_entity = SourceEntity()
#             source_entity.source = source
#             source_entity.save()

#             if index == 1:
#                 for order, key in enumerate(row.keys()):
#                     try:
#                         source_field = SourceField.objects.filter(
#                             source=source).get(name=key)
#                     except SourceField.DoesNotExist:
#                         source_field = SourceField()
#                     source_field.source = source
#                     source_field.name = key
#                     source_field.display_order = order
#                     source_field.save()

#             for field in row.keys():
#                 source_field = SourceField.objects.filter(
#                     source=source).get(name=field)
#                 try:
#                     source_value = SourceValue.objects.filter(
#                         source_field=source_field).get(value=row[field])
#                 except SourceValue.DoesNotExist:
#                     source_value = SourceValue()
#                 source_value.source_field = source_field
#                 source_value.value = row[field]
#                 source_value.save()

#                 try:
#                     source_data = SourceData.objects.filter(source_entity=source_entity).filter(
#                         source_field=source_field).get(source_value=source_value)
#                 except SourceData.DoesNotExist:
#                     source_data = SourceData()
#                 source_data.source_entity = source_entity
#                 source_data.source_field = source_field
#                 source_data.source_value = source_value
#                 source_data.save()


# def print_progress(index, rows):
#     div = rows//5
#     if index % div == 0 and div != 0:
#         print(f"Processing... ({(2*index)//div}0% done)")


# def save_uploaded_file(f):
#     try:
#         os.mkdir(os.path.join(settings.MEDIA_ROOT, 'masterdata'))
#     except:
#         pass

#     path_to_file = os.path.join(settings.MEDIA_ROOT, 'masterdata', f.name)
#     with open(path_to_file, 'wb+') as destination:
#         for chunk in f.chunks():
#             destination.write(chunk)
