from __future__ import unicode_literals
from django.db import models
import jsonfield

# from django_mysql.models import JSONField
from django.views.generic import ListView


class Json_TableQuerySet(models.QuerySet):
    def delete(self, *args, **kwargs):
        for obj in self:
            obj.table.delete()
        super(Json_TableQuerySet, self).delete(*args, **kwargs)


class Json_Table(models.Model):
    user_id = models.IntegerField(null=True)
    pdf_id = models.IntegerField(null=True)
    page_number = models.IntegerField(null=True)
    json_table = models.JSONField()
    table = models.FileField(upload_to="json/", max_length=500)

    def delete(self, *args, **kwargs):
        self.table.delete()
        super(Json_Table, self).delete(*args, **kwargs)

<<<<<<< HEAD
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
=======

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
>>>>>>> d1d59e1889d4ec32d85c111bc49805e6bdfdeeb0
p