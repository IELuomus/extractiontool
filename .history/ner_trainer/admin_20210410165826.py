from django.contrib import admin
from .models import TraitnameLearnData




class TraitnameLearnDataAdmin(admin.ModelAdmin):
    list_display = ('data',)

admin.site.register(Json_Table, JsonTableAdmin)
admin.site.register(Trait_Table)
# Register your models here.
