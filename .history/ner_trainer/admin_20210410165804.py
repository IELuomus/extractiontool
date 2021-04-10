from django.contrib import admin
from .models import TraitnameLearnData




class TraitTableAdmin(admin.ModelAdmin):
    list_display = ('trait_table',)

admin.site.register(Json_Table, JsonTableAdmin)
admin.site.register(Trait_Table)
# Register your models here.
