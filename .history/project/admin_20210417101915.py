from django.contrib import admin

# Register your models here.
from .models import Json_Table, Trait_Table
from django.contrib.sites.models import Site

class TraitTableAdmin(admin.ModelAdmin):
    list_display = ('trait_table',)

admin.site.register(Json_Table, JsonTableAdmin)
admin.site.register(Trait_Table)