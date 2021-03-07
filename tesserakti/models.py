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


class Page(models.Model):
    page_id = models.IntegerField(db_index=True)
    document_id = models.IntegerField(db_index=True)
    vasen = models.IntegerField(db_index=True)
    top = models.IntegerField(db_index=True)
    width = models.IntegerField(db_index=True)
    height = models.IntegerField(db_index=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'tes_page'
        unique_together = (('page_id', 'document_id'),)


class Block(models.Model):
    block_id = models.IntegerField(db_index=True)
    page_id = models.IntegerField(db_index=True)
    document_id = models.IntegerField(db_index=True)
    vasen = models.IntegerField(db_index=True)
    top = models.IntegerField(db_index=True)
    width = models.IntegerField(db_index=True)
    height = models.IntegerField(db_index=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'tes_block'
        unique_together = (('block_id', 'page_id', 'document_id'),)


class Paragraph(models.Model):
    paragraph_id = models.IntegerField(db_index=True)
    block_id = models.IntegerField(db_index=True)
    page_id = models.IntegerField(db_index=True)
    document_id = models.IntegerField(db_index=True)
    vasen = models.IntegerField(db_index=True)
    top = models.IntegerField(db_index=True)
    width = models.IntegerField(db_index=True)
    height = models.IntegerField(db_index=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'tes_paragraph'
        unique_together = (('paragraph_id', 'block_id', 'page_id', 'document_id'),)


class Line(models.Model):
    line_id = models.IntegerField(db_index=True)
    paragraph_id = models.IntegerField(db_index=True)
    block_id = models.IntegerField(db_index=True)
    page_id = models.IntegerField(db_index=True)
    document_id = models.IntegerField(db_index=True)
    vasen = models.IntegerField(db_index=True)
    top = models.IntegerField(db_index=True)
    width = models.IntegerField(db_index=True)
    height = models.IntegerField(db_index=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'tes_line'
        unique_together = (('line_id', 'paragraph_id', 'block_id', 'page_id', 'document_id'),)


class Word(models.Model):
    word_id = models.IntegerField(db_index=True)
    line_id = models.IntegerField(db_index=True)
    paragraph_id = models.IntegerField(db_index=True)
    block_id = models.IntegerField(db_index=True)
    page_id = models.IntegerField(db_index=True)
    document_id = models.IntegerField(db_index=True)
    vasen = models.IntegerField(db_index=True)
    top = models.IntegerField(db_index=True)
    width = models.IntegerField(db_index=True)
    height = models.IntegerField(db_index=True)
    conf = models.IntegerField(db_index=True)
    text = models.CharField(max_length=200, db_index=True)
    created = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'tes_word'
        unique_together = (('word_id', 'line_id', 'paragraph_id', 'block_id', 'page_id', 'document_id'),)
