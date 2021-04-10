from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from spacy_parse.views import (
  parse
)

urlpatterns = [
  path('<int:pk>/', parse, name='parse'),
   url(r'^signup/$', views.SignUpView.as_view(), name='signup'),
  #path('parse/<int:pk>/', parse, name='parse'),
  # url(r'^health$', health),
  # path('upload/', include('project.urls')),
    
]