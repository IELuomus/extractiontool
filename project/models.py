from django.db import models

from document.models import Pdf

# Create your models here.

class TraitTable(models.Model):
    pdf_id = models.ForeignKey(Pdf, on_delete=models.CASCADE)
    verbatimScientificName = models.CharField(max_length=100, null=True)
    verbatimTraitName = models.CharField(max_length=100)
    verbatimTraitValue = models.CharField(max_length=100)
    verbatimTraitUnit = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=100, null=True)

    def delete(self, *args, **kwargs):
        super(TraitTable, self).delete(*args, **kwargs)

# class Trait_TableQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for obj in self:
#             obj.table.delete()
#         super(Trait_TableQuerySet, self).delete(*args, **kwargs)
