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

# from document.uploadhandler import DocumentFileUploadHandler
import subprocess
import fitz
import os
from django.core.files import File

# def dynamic_path(instance, filename):
#     return f'pdf/{instance.sha1sum}/{filename}'

def get_sha1sum(file_path):
    # find out sha1sum
    command_result = subprocess.run(['sha1sum', f"{file_path}"], stdout=subprocess.PIPE)
    sum=command_result.stdout.decode('utf-8').split()[0]
    return sum

def get_filesize(file_path):
    # find out filesize
    command_result = subprocess.run(['stat', '--printf=%s',f"{file_path}"], stdout=subprocess.PIPE)
    file_size=int(command_result.stdout.decode('utf-8'))
    return file_size

def get_pagecount(file_path):
    # find out pagecount
    pagecount=fitz.open(f'{file_path}').pageCount
    return pagecount

class Pdf(models.Model):


    file = models.FileField(upload_to="pdf")
    filename = models.CharField(max_length=1000)
    size = models.IntegerField()
    sha1sum = models.CharField(max_length=40, unique=True)
    pagecount = models.IntegerField()
    created = models.DateTimeField(default=timezone.now)

    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)

    class Meta:
        managed = True
        db_table = 'doc_pdf'

    def save(self, *args, **kwargs):
        if self.pk is not None:
            # file already existed.
            super(Pdf, self).save(*args, **kwargs)
        else:
            # new file upload.
            sha1sum = get_sha1sum(self.file)
            print(f'sha1sum: {sha1sum}')      

            # check if the same document is already uploaded
            if Pdf.objects.filter(sha1sum=sha1sum).first() is None:
                # file does not already exist.
                filename = os.path.basename(str(self.file))

                filesize = get_filesize(self.file)
                print(f'filesize: {filesize}')                        
                pagecount = get_pagecount(self.file)
                print(f'pagecount: {pagecount}')          
                self.filename = filename              
                self.sha1sum = sha1sum
                self.size = filesize
                self.pagecount = pagecount
                final_path = f'{self.sha1sum}/{os.path.basename(str(self.file))}'

                self.file.name = final_path

                super(Pdf, self).save(*args, **kwargs)
                current_user_id=1 # TODO: hae jostain
                DocumentOwner.objects.create(document=self, owner=User.objects.get(id=current_user_id))
            else:
                # file exists.
                existing_document = Pdf.objects.filter(sha1sum=sha1sum).first()
                # check if doc_owner row already exists.
                current_user_id=1 # TODO: hae jostain
                existing_owner = DocumentOwner.objects.filter(document=existing_document, owner=User.objects.get(id=current_user_id))
                if existing_owner is None:
                    DocumentOwner.objects.create(document=existing_document, owner=User.objects.get(id=current_user_id))

    def _str_(self):
        return self.title

    def delete(self, *args, **kwargs):
        # TODO: delete documentOwner here and pdf only if no owners left.
        self.pdf.delete()
        super().delete(*args, **kwargs)

class DocumentOwner(models.Model):
    document = models.ForeignKey(Pdf, on_delete=CASCADE)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    upload_date = models.DateTimeField(default=timezone.now)

    class Meta:
        managed = True
        db_table = 'doc_owner'
        
        unique_together = (('document', 'owner'),)
