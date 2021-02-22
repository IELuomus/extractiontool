from django.db import models
from django.db.models.deletion import CASCADE


class Source(models.Model):
    name = models.CharField(max_length=255)


class SourceEntity(models.Model):
    source = models.ForeignKey(Source, on_delete=CASCADE)


class SourceField(models.Model):
    name = models.CharField(max_length=255)
    display_order = models.IntegerField()
    source = models.ForeignKey(Source, on_delete=CASCADE)

    class Meta:
        ordering = ["display_order"]


class SourceValue(models.Model):
    value = models.TextField()
    source_field = models.ForeignKey(SourceField, on_delete=CASCADE)


class SourceData(models.Model):
    source_entity = models.ForeignKey(SourceEntity, on_delete=CASCADE)
    source_field = models.ForeignKey(SourceField, on_delete=CASCADE)
    source_value = models.ForeignKey(SourceValue, on_delete=CASCADE)
