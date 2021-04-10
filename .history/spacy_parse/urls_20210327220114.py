from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from spacy_parse.views import (
  parse, traitvalues
)

urlpatterns = [
  path('<int:pk>/', parse, name='parse'),
  path('<int:pk>/'traitvalues/', traitvalues)
  #path('parse/<int:pk>/', parse, name='parse'),
  # url(r'^health$', health),
  # path('upload/', include('project.urls')),
    
]