from django.contrib import admin
from .models import TraitnameLearnData




class TraitnameLearnDataAdmin(admin.ModelAdmin):
    list_display = ('data',)

admin.site.register(TraitnameLearnData, Tra)
# Register your models here.
