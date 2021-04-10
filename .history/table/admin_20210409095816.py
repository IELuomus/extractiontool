from django.contrib import admin

# Register your models here.
from .models import Json_Table, Trait_Table


class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table', 'trait_table')

class TraitTableAdmin(admin.ModelAdmin):
    list_display = ('trait_table')

admin.site.register(Json_Table, Trait_Table, JsonTableAdmin)
admin.site.register(Trait_Table, TraitTableAdmin)