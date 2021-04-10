from __future__ import unicode_literals
from django.db import models
import jsonfield
# Create your models here.
from django_mysql.models import JSONField


class Json_TableQuerySet(models.QuerySet):
    
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.table.delete()
        super(Json_TableQuerySet, self).delete(*args, **kwargs)


class Json_Table(models.Model):
    json_table= models.JSONField()
    table = models.FileField(upload_to='json/')
    
    def delete(self, *args, **kwargs):
        self.table.delete()
        super(Json_Table, self).delete(*args, **kwargs)


class Trait_Table(models.Model):
    pdf_id = models.IntegerField(null=True)
    scientific_name = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=100)
    trait_name = models.CharField(max_length=100)
    trait_value = models.CharField(max_length=100)
    trait_unit = models.CharField(max_length=100)
    

    def delete(self, *args, **kwargs):
        super(Trait_Table, self).delete(*args, **kwargs)


class Trait_TableQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.table.delete()
        super(Trait_TableQuerySet, self).delete(*args, **kwargs)