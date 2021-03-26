from __future__ import unicode_literals
from django.db import models
import jsonfield
# Create your models here.
from django_mysql.models import JSONField
from django_editorjs import EditorJsField
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

class Edit_Text(models.Model):
    title = models.TextField()
    body = EditorJsField(
        editorjs_config={
            "tools": {
                "Table": {
                    "disabled": True,
                    "inlineToolbar": True,
                    "config": {"rows": 2, "cols": 3,},
                }
            }
        }
    )