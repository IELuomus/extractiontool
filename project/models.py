from django.db import models

# Create your models here.

class Pdf(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs/')

    def _str_(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.pdf.delete()
        super().delete(*args, **kwargs)

class Trait_Table(models.Model):
    pdf_id = models.ForeignKey(Pdf)
    verbatimScientificName = models.CharField(max_length=100, null=True)
    verbatimTraitName = models.CharField(max_length=100)
    verbatimTraitValue = models.CharField(max_length=100)
    verbatimTraitUnit = models.CharField(max_length=100)
    sex = models.CharField(max_length=100, null=True)

    def delete(self, *args, **kwargs):
        super(Trait_Table, self).delete(*args, **kwargs)

# class Trait_TableQuerySet(models.QuerySet):
#     def delete(self, *args, **kwargs):
#         for obj in self:
#             obj.table.delete()
#         super(Trait_TableQuerySet, self).delete(*args, **kwargs)

