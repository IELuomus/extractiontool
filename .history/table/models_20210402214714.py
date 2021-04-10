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
    user_id = models.IntegerField()
    user_id = models.IntegerField()
    json_table= models.JSONField()
    table = models.FileField(upload_to='json/')
    
    def delete(self, *args, **kwargs):
        self.table.delete()
        super(Json_Table, self).delete(*args, **kwargs)