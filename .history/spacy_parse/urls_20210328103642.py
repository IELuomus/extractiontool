from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from spacy_parse.views import (
  parse, ajax_url
)

urlpatterns = [
  path('<int:pk>/', parse, name='parse'),
  path('ajax_url/', ajax_view_for_ajax_url, name='ajax_url')
  # path('<int:pk>/traitvalues/', traitvalues)
  #path('parse/<int:pk>/', parse, name='parse'),
  # url(r'^health$', health),
  # path('upload/', include('project.urls')),
    
]