from django.contrib import admin

# Register your models here.
<<<<<<< HEAD
from .models import Json_Table, Edit_Text

=======
from .models import Json_Table, Trait_Table
from django.contrib.sites.models import Site
>>>>>>> d1d59e1889d4ec32d85c111bc49805e6bdfdeeb0

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

<<<<<<< HEAD
admin.site.register(Json_Table, JsonTableAdmin)

@admin.register(Edit_Text)
class Edit_TextAdmin(admin.ModelAdmin):
    pass
=======
# admin.site.register(Site, SiteAdmin)
>>>>>>> d1d59e1889d4ec32d85c111bc49805e6bdfdeeb0
