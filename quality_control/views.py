from django.utils import timezone
from django.contrib import messages
from users.views import user_is_data_admin_or_editor
from django.template.defaulttags import register
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


@login_required
@user_passes_test(user_is_data_admin_or_editor)
# @remember_last_query_params('quality-control-list', ['page', 'workflow', 'status'])
def quality_control_list(request):
    workflows = Workflow.objects.all()
    if request.GET.get('workflow'):
        workflow = Workflow.objects.get(pk=request.GET.get('workflow'))
    else:
        workflow = Workflow.objects.get(pk=6400)
    query = request.GET.get('query')
    status = request.GET.get('status')
    whole_query = f"?query={query}&workflow={workflow.id}&status={status}"
    retirements = get_retirements(request, workflow)
    tasks = get_tasks_for_workflow(workflow)
    values, colors = get_counts_and_colors(retirements, tasks)
    return render(request, 'quality_control/quality_control_list.html',
                  {'workflows': workflows,
                   'current_workflow': workflow,
                   'page_obj': retirements,
                   'tasks': tasks,
                   'values': values,
                   'colors': colors,
                   'status': status,
                   'whole_query': whole_query})


# @login_required
# @user_passes_test(user_is_data_admin_or_editor)
# def quality_control_check(request, workflow_pk, scan_pk):
#     workflow = Workflow.objects.get(pk=workflow_pk)
#     scan = Scan.objects.get(id=scan_pk)
#     prev_scan, next_scan = get_next_and_prev_scans(request, scan)
#     retirement = scan.subject.retirement_set.filter(workflow=workflow).first()
#     tasks = get_tasks_for_workflow(workflow)
#     workflows, all_checked = get_all_workflows(scan)

#     if request.method == 'POST':
#         if 'waiting-btn' in request.POST:
#             retirement.status = 'waiting'
#             retirement.save()
#             messages.success(request, "Status set as waiting")
#             return redirect('quality-control-check', scan_pk=scan_pk, workflow_pk=workflow_pk)
#         retirement.status = 'checked'
#         retirement.checked_on = timezone.now()
#         retirement.checked_by = request.user
#         retirement.save()
#         for question in tasks.values():
#             answer = request.POST.get(question, None)
#             if answer:
#                 final = FinalAnnotation()
#                 final.scan = scan
#                 final.retirement = retirement
#                 final.question = question
#                 final.answer = answer
#                 final.save()
#         return redirect('quality-control-check', scan_pk=scan.id, workflow_pk=workflow.id)
#     checked = retirement.status == 'checked'
#     if not checked:
#         questions = get_questions_and_values(retirement, tasks)
#     else:
#         questions = get_final_annotations(retirement, tasks)
#     return render(request, 'quality_control/quality_control_check.html',
#                   {'current_workflow': workflow,
#                    'scan': scan,
#                    'prev_scan': prev_scan,
#                    'next_scan': next_scan,
#                    'questions': questions,
#                    'checked': checked,
#                    'workflows': workflows,
#                    'all_checked': all_checked})


# @login_required
# @user_passes_test(user_is_data_admin_or_editor)
# @remember_last_query_params('summary-list', ['page'])
# def summary_list(request):
#     workflows = Workflow.objects.all()
#     scans = get_scans(request)
#     statuses = {}
#     for scan in scans:
#         workflows_dict = {}
#         try:
#             retirements = scan.subject.retirement_set.all()
#             for workflow in workflows:
#                 if len(retirements.filter(workflow=workflow)) == 0:
#                     workflows_dict[workflow] = {
#                         'status': 'NA', 'color': 'grey'}
#                 else:
#                     r = retirements.filter(workflow=workflow).first()
#                     workflows_dict[workflow] = {'status': r.status}
#                     if r.status == 'checked':
#                         workflows_dict[workflow]['color'] = 'green'
#                     elif r.status == 'waiting':
#                         workflows_dict[workflow]['color'] = 'yellow'
#                     else:
#                         workflows_dict[workflow]['color'] = 'red'
#         except Subject.DoesNotExist:
#             for workflow in workflows:
#                 workflows_dict[workflow] = {'status': 'NA', 'color': 'grey'}
#         statuses[scan] = workflows_dict
#     return render(request, 'quality_control/summary_list.html',
#                   {'workflows': workflows,
#                    'statuses': statuses,
#                    'page_obj': scans})


# @login_required
# @user_passes_test(user_is_data_admin_or_editor)
# def summary_check(request, scan_pk):
#     scan = Scan.objects.get(pk=scan_pk)
#     if request.method == 'POST':
#         if 'add-field-btn' in request.POST:
#             field_name = request.POST.get('field-name', '')
#             try:
#                 AnnotationField.objects.get(name=field_name)
#             except AnnotationField.DoesNotExist:
#                 if field_name:
#                     field = AnnotationField()
#                     field.name = field_name
#                     field.save()
#             messages.success(request, "Field added")
#         elif 'add-content-btn' in request.POST:
#             field_name = request.POST.get('field', '')
#             field_content = request.POST.get('field-content', '')
#             final_annotation = scan.finalannotation_set.filter(
#                 question=field_name).first()
#             if final_annotation:
#                 final_annotation.answer = field_content
#                 final_annotation.save()
#             else:
#                 final_annotation = FinalAnnotation()
#                 final_annotation.scan = scan
#                 final_annotation.question = field_name
#                 final_annotation.answer = field_content
#                 final_annotation.save()
#         elif 'confirm-scan' in request.POST:
#             scan.status = "FINISHED"
#             scan.save()
#         return redirect('summary-check', scan_pk=scan.id)
#     try:
#         prev_scan = Scan.objects.get(pk=scan_pk-1)
#     except Scan.DoesNotExist:
#         prev_scan = None
#     try:
#         next_scan = Scan.objects.get(pk=scan_pk+1)
#     except Scan.DoesNotExist:
#         next_scan = None
#     workflows, all_checked = get_all_workflows(scan)
#     annotations = FinalAnnotation.objects.filter(scan=scan)
#     fields = AnnotationField.objects.all()
#     return render(request, 'quality_control/summary_check.html',
#                   {'scan': scan,
#                    'prev_scan': prev_scan,
#                    'next_scan': next_scan,
#                    'annotations': annotations,
#                    'workflows': workflows,
#                    'fields': fields,
#                    'all_checked': all_checked})


# def get_retirements(request, workflow):
#     query = request.GET.get('query')
#     status = request.GET.get('status')
#     retirement_list = Retirement.objects.filter(workflow=workflow)
#     if status:
#         retirement_list = retirement_list.filter(status=status)
#     if query:
#         try:
#             query = int(query)
#             scan = Scan.objects.get(pk=query)
#             subject = scan.subject
#             retirement_list = retirement_list.filter(subject=subject)
#         except:
#             pass
#     retirement_list = retirement_list.order_by('subject__scan__id')
#     page = request.GET.get('page', 1)
#     paginator = Paginator(retirement_list, 10)
#     try:
#         retirements = paginator.page(page)
#     except PageNotAnInteger:
#         retirements = paginator.page(1)
#     except EmptyPage:
#         retirements = paginator.page(paginator.num_pages)
#     return retirements


# def get_scans(request):
#     query = request.GET.get('query')
#     if query:
#         scans_list = Scan.objects.filter(pk=query)
#     else:
#         scans_list = Scan.objects.all()
#     page = request.GET.get('page', 1)
#     paginator = Paginator(scans_list, 15)
#     try:
#         scans = paginator.page(page)
#     except PageNotAnInteger:
#         scans = paginator.page(1)
#     except EmptyPage:
#         scans = paginator.page(paginator.num_pages)
#     return scans


# def get_next_and_prev_scans(request, scan):
#     print(request.session.keys())
#     workflow_id = request.session.get('quality-control-list_workflow', 6400)
#     workflow = Workflow.objects.get(pk=workflow_id)
#     status = request.session.get(
#         'quality-control-list_status', 'to be checked')
#     retirement_list = Retirement.objects.filter(workflow=workflow)
#     retirement_list = retirement_list.filter(status=status)
#     prev_item = retirement_list.filter(
#         subject__scan__id__lt=scan.id).order_by('-subject__scan__id')[:1].first()
#     next_item = retirement_list.filter(
#         subject__scan__id__gt=scan.id).order_by('subject__scan__id')[:1].first()
#     prev_scan = prev_item.subject.scan if prev_item else None
#     next_scan = next_item.subject.scan if next_item else None
#     return prev_scan, next_scan


# def get_counts_and_colors(retirements, tasks):
#     counts = dict()
#     colors = dict()
#     for retirement in retirements:
#         counts[retirement] = len(retirement.classification_set.all())
#         colors[retirement] = []
#         for task in tasks:
#             classifications = retirement.classification_set.all()
#             annotations = []
#             for classification in classifications:
#                 annotations.extend(
#                     classification.annotation_set.filter(task=task))
#             answer_counts = {}
#             for annotation in annotations:
#                 answer_counts[annotation.value] = answer_counts.get(
#                     annotation.value, 0) + 1
#             if answer_counts:
#                 max_count = max(answer_counts.values())
#                 similarity_score = max_count / len(annotations)
#                 if similarity_score <= 1/len(annotations):
#                     colors[retirement].append('red')
#                 elif similarity_score < 0.5:
#                     colors[retirement].append('orange')
#                 elif similarity_score < 1:
#                     colors[retirement].append('yellow')
#                 else:
#                     colors[retirement].append('green')
#             else:
#                 colors[retirement].append('red')
#     return counts, colors


# def get_tasks_for_workflow(workflow):
#     if workflow.name == 'Specimen Numbers':
#         header = ['Pfx', 'AN', 'FN', 'FN (Pre)', 'Shelf',
#                   'Date', 'Published', 'Type', 'PTO']
#         tasks = ['T9', 'T1', 'T2', 'T5', 'T8', 'T6', 'T3', 'T7', 'T4']
#     elif workflow.name == 'Location and stratigraphy':
#         header = ['Locality', 'SITE/AREA', 'Formation',
#                   'Mbr/Horizon/Etc.', 'Photo', 'Coordinates']
#         tasks = ['T0', 'T3', 'T2', 'T1', 'T5', 'T7']
#     elif workflow.name == 'Nature of Specimen (Body parts)':
#         header = ['Body parts', 'Fragments']
#         tasks = ['T0', 'T1']
#     elif workflow.name == 'Specimen Taxonomy (Latin names)':
#         header = ['Taxon', 'Family', 'Subfamily', 'Tribe', 'Genus', 'Species']
#         tasks = ['T0', 'T2', 'T3', 'T1', 'T4', 'T5']
#     elif workflow.name == 'Additional info (Card backside)':
#         header = ['Reference', 'Coordinates', 'Photo', 'Other']
#         tasks = ['T4', 'T5', 'T6', 'T7']
#     else:
#         header = []
#         tasks = []
#     return {tasks[i]: header[i] for i in range(len(tasks))}


# def get_all_workflows(scan):
#     workflows = Workflow.objects.all()
#     all_workflows = []
#     all_checked = True
#     for workflow in workflows:
#         retirement = scan.subject.retirement_set.filter(
#             workflow=workflow).first()
#         if retirement is None:
#             all_checked = False
#             all_workflows.append((workflow, None))
#         else:
#             status = retirement.status
#             if status != 'checked':
#                 all_checked = False
#             all_workflows.append((workflow, status))
#     return all_workflows, all_checked


# def get_final_annotations(retirement, tasks):
#     questions = []
#     annotations = FinalAnnotation.objects.filter(retirement=retirement)
#     for task, name, in tasks.items():
#         annotation = annotations.filter(question=name).first()
#         if annotation:
#             answers = {annotation.answer: 1}
#             color = 'grey'
#             questions.append({name: [answers, color, 1]})
#     return questions


# def get_questions_and_values(retirement, tasks):
#     questions = []
#     for task, name in tasks.items():
#         classifications = retirement.classification_set.all()
#         annotations = []
#         for classification in classifications:
#             annotations.extend(
#                 classification.annotation_set.filter(task=task))
#         answers = {}
#         for annotation in annotations:
#             answers[annotation.value] = answers.get(
#                 annotation.value, 0) + 1
#         answers = {k: v for k, v in sorted(
#             answers.items(), key=lambda item: item[1], reverse=True)}
#         if answers:
#             max_count = max(answers.values())
#             similarity_score = max_count / len(annotations)
#             if similarity_score <= 1/len(annotations):
#                 color = 'red'
#             elif similarity_score <= 0.5:
#                 color = 'orange'
#             elif similarity_score < 1:
#                 color = 'yellow'
#             else:
#                 color = 'green'
#         else:
#             answers[''] = 1
#             color = 'red'
#         first_value = get_first_value(answers)
#         questions.append({name: [answers, color, first_value]})
#     return questions


# def get_first_value(dictionary):
#     values = dictionary.keys()
#     iterator = iter(values)
#     first_value = next(iterator)
#     return first_value


# @ register.filter
# def get_item(dictionary, key):
#     return dictionary.get(key)
