from __future__ import unicode_literals
from django.db import models
import jsonfield
# Create your models here.
from django_mysql.models import JSONField

class Json_Table(models.Model):
    json_table= models.JSONField()
    # created_by = models.CharField(max_length=50)
    table = models.FileField(upload_to='json/')

    def _str_(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.json_table.delete()
        super().delete(*args, **kwargs)