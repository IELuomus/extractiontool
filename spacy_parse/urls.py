from django.urls import path
from django.conf.urls import url
from project.views import health
from spacy_parse.views import (
  parse
)

urlpatterns = [
  path('parse/', parse, name='parse'),
  url(r'^health$', health),
    
]