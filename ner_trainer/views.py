from django.shortcuts import render
import json
from .forms import TraitValuesForm
from django.views.generic.edit import CreateView
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from django.http import HttpResponse

@require_GET
def ajax_url(request):
  
    print("ajax: ")
    
    if request.method == 'GET':
            response_json = request.GET
            response_json = json.dumps(response_json)
            data = json.loads(response_json)
            print(data)
            for key, value in data.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
                print(key)
                print('value: ', str(value))
    # if request.method == 'POST':
    #     print("fetch")
    #     response_json = request.POST
    #     response_json = json.dumps(response_json)
    #     data2 = json.loads(response_json)
    #     print(data2)

    return JsonResponse(data)

