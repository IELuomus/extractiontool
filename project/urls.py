from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from django.urls.conf import include
from users.views import index
from .views import *
from table.views import table_to_dataframe

urlpatterns = [
    path('pdfs/', pdf_list, name='pdf_list'),
    path('pdfs/<int:pk>/', delete_pdf, name='delete_pdf'),
    path('pdfs/upload/', upload_pdf, name='upload_pdf'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')),
    path('page_number/',table_to_dataframe),
    path('page_number/<int:pk>', table_to_dataframe, name="page_number"),
    path('quality_control/', include('quality_control.urls')),
    path('masterdata/', include('masterdata.urls')),
    path('', index, name='index'),
    url(r'^health$', health),
    path('table/', include('table.urls')),
    path('parse/', include('spacy_parse.urls')),
    path('', index, name='index'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
