from django.contrib import admin

# Register your models here.
from .models import Json_Table, Trait_Table


class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table',)

class TraitTableAdmin(admin.ModelAdmin):
    list_display = ('trait_table',)

admin.site.register(Json_Table, JsonTableAdmin)
from django.contrib.sites.models import Site


admin.site.register(Trait_Table)

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('pdf_id', 'scientific_name', 'trait_name', 'trait_value', 'trait_unit')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')
admin.site.register(Site, SiteAdmin)