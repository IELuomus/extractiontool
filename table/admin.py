from django.contrib import admin

# Register your models here.
from .models import Json_Table, Edit_Text


class JsonTableAdmin(admin.ModelAdmin):
    list_display = ('json_table',)


admin.site.register(Json_Table, JsonTableAdmin)

@admin.register(Edit_Text)
class Edit_TextAdmin(admin.ModelAdmin):
    pass