from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from ner_trainer.views import (
   ajax_url
)

urlpatterns = [
  #path('ner_trainer/ajax_url/', ajax_url, name='ajax_url')
  path('ajax_url/', ajax_url, name='ajax_url')
    
]