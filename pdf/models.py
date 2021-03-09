# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = True` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils import timezone
import pytz
from django.db.models import CASCADE
from users.models import User


class Document(models.Model):
    filename = models.CharField(max_length=1000)
    size = models.IntegerField()
    sha1sum = models.CharField(max_length=40)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        


class DocumentOwner(models.Model):
    document = models.ForeignKey(Document, on_delete=CASCADE)
    # document_id = models.IntegerField()
    owner = models.ForeignKey(User, on_delete=CASCADE)
    # owner_id = models.IntegerField()
    upload_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        
        unique_together = (('document', 'owner'),)
        # unique_together = (('document_id', 'owner_id'),)
