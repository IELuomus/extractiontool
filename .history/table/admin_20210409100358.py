from django.contrib import admin

# Register your models here.
from .models import Json_Table, Trait_Table


class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table',)

class TraitTableAdmin(admin.ModelAdmin):
    list_display = ('trait_table',)

admin.site.register(Json_Table, JsonTableAdmin)
from django.contrib.sites.models import Site


admin.site.register(User)

admin.site.unregister(Site)
class SiteAdmin(admin.ModelAdmin):
    fields = ('pdf_id', 'scientific_name', 'doma')
    readonly_fields = ('id',)
    list_display = ('id', 'name', 'domain')
    list_display_links = ('name',)
    search_fields = ('name', 'domain')
admin.site.register(Site, SiteAdmin)