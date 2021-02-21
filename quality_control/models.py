from django.db import models
from django.db.models.deletion import PROTECT
from django_userforeignkey.models.fields import UserForeignKey
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import ForeignKey


# class FinalAnnotation(models.Model):
#     scan = ForeignKey(Scan, on_delete=CASCADE)
#     retirement = ForeignKey(Retirement, on_delete=CASCADE, null=True)
#     question = models.CharField(max_length=255, blank=True)
#     answer = models.TextField(blank=True)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     created_by = UserForeignKey(auto_user_add=True, on_delete=PROTECT,
#                                 related_name='added_final_annotations')
#     modified_by = UserForeignKey(auto_user=True, on_delete=PROTECT,
#                                  related_name='modified_final_annotations')


# class AnnotationField(models.Model):
#     name = models.CharField(max_length=255)
#     created_on = models.DateTimeField(auto_now_add=True)
#     modified_on = models.DateTimeField(auto_now=True)
#     created_by = UserForeignKey(auto_user_add=True, on_delete=PROTECT,
#                                 related_name='added_annotation_fields')
#     modified_by = UserForeignKey(auto_user=True, on_delete=PROTECT,
#                                  related_name='modified_annotation_fields')

#     class Meta:
#         ordering = ["name"]
