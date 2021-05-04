from django.contrib import admin

from .models import Json_Table 
from django.contrib.sites.models import Site

class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table',)

admin.site.register(Json_Table, JsonTableAdmin)

