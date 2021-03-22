from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from .views import (
  table_to_dataframe, redirect_form
)


urlpatterns = [
  path('table/', table_to_dataframe, name="table"),
  # path('page_number/<int:pk>', table_to_dataframe, name="page_number"),
  # path('page_number/$',table_to_dataframe),
  path('redirect_form/<int:pk>', redirect_form, name='redirect_form'),
  #path('parse/<int:pk>/', parse, name='parse'),
  url(r'^health$', health),
    
]