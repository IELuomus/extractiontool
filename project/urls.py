from django.conf import settings
from django.conf.urls import url
from django.contrib import admin

from django.contrib.auth import logout

from django.urls import path, include
from .views import homePageView, index, health, myView


urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^health$', health),
    path('', homePageView, name='home'),
    path('accounts/', include('allauth.urls')),
    path('index', myView, name='index'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')


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
