from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from spacy_parse.views import (
  parse, TraitValueView
)

urlpatterns = [
  path('<int:pk>/', parse, name='parse'),
  path('traitvalues/')
  url(r'^traitvalues/$', TraitValueView.as_view(), name='traitvalues'),
  #path('parse/<int:pk>/', parse, name='parse'),
  # url(r'^health$', health),
  # path('upload/', include('project.urls')),
    
]