from django.urls import path
from django.conf.urls import url
from project.views import health
from django.urls.conf import include
from .views import (
  table_to_dataframe, redirect_form, json_table_list, post_url
)


urlpatterns = [
<<<<<<< HEAD
  path('table/', table_to_dataframe, name='table'),
  path('redirect_form/<int:pk>', redirect_form, name='redirect_form'),
  url(r'^health$', health),
=======
  path('table/', table_to_dataframe, name="table"),
  path('redirect_form/<int:pk>', redirect_form, name='redirect_form'),
  path('selected_tables/<int:user_id>/<int:pdf_id>/<int:page_number>/', json_table_list, name='selected_tables'),
  path('table/post_url/', post_url, name='post_url'),
  url(r'^health$', health),    
>>>>>>> d1d59e1889d4ec32d85c111bc49805e6bdfdeeb0
]