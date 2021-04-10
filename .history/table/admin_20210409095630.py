from django.contrib import admin

# Register your models here.
from .models import Json_Table, Trait_Table


class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table',)


admin.site.register(Json_Table, JsonTableAdmin)