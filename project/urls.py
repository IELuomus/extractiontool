from django.conf import settings
from django.conf.urls import url
from django.contrib import admin


from django.urls import path, include
from .views import homePageView, index, health, upload


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^health$', health),
    path('', homePageView, name='home'),
    path('accounts/', include('allauth.urls')),
    path('', index, name='index'),
    # path('health/', health),
    url(r'^health$', health),
    # url(r'^ht/', include('health_check.urls')),
    path('upload/', upload, name='upload'),

]



#urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^$', index),
    #url(r'^health$', health),
    #path('admin/', include('admin.site.urls'))
    #url(r'^admin/', admin.site.urls),
#]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)