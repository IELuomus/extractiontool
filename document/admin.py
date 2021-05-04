from django.contrib import admin

from .models import Pdf


class PdfAdmin(admin.ModelAdmin):
    list_display = ("title", "author")

admin.site.register(Pdf, PdfAdmin)
