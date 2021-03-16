from django.db import models

# Create your models here.

class Pdf(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='pdfs/')

    def _str_(self):
        return self.title