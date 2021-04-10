from django.contrib import admin

# Register your models here.
from .models import Json_Table, Trait_Table
from django.contrib.sites.models import Site

class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table',)

class TraitTableAdmin(admin.ModelAdmin):
    list_display = ('trait_table',)

admin.site.register(Json_Table, JsonTableAdmin)
admin.site.register(Trait_Table)
# admin.site.unregister(Site)

# class SiteAdmin(admin.ModelAdmin):
#     fields = ('pdf_id', 'scientific_name', 'trait_name', 'trait_value', 'trait_unit', 'sex')
#     readonly_fields = ('id',)
#     list_display = ( 'scientific_name',)
#     search_fields = ('scientific_name',)

# admin.site.register(Site, SiteAdmin)
