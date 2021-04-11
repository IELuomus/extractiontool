from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from ner_trainer.views import (
   fetch_url
)

urlpatterns = [
  path('fetch_url/', fetch_url, name='fetch_url')
    
]