# batch script which uploads all the .pdf documents in a directory structure.
import os
import django
# needed for headless script only.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # project/settings.py
django.setup()
from tesserakti.models import Word, Page, Block, Paragraph, Line
from document.models import Pdf, DocumentTask, DocumentOwner
from document.document_util import *
import multiprocessing as mp
from tesserakti.task_imagemagic import TaskImageMagick
from tesserakti.task_tesseract import TaskTesseract
from tesserakti.task_tesseract_OCR import TaskTesseractOCR
from tesserakti.tessera_util import set_up_document_background_image_tasks
import sys
import time
from pathlib import Path
from django_q.tasks import async_task, schedule
import logging
from django.conf import settings

print("Number of processors: ", mp.cpu_count())

# to make things easier delete everything..
for malli in (DocumentTask, DocumentOwner, Word, Line, Paragraph, Block, Page, Pdf):
    queryset = malli.objects.all()
    queryset._raw_delete(queryset.db)

# tiedostojen_polku='../all_testfiles/'
tiedostojen_polku='../some_testfiles'

# create documents to database ( and copy under media/pdf/<sha1sum>/ )
for document_file in Path(tiedostojen_polku).glob("**/*.pdf"):
    owner_id=1
    create_document_from_pdf_file(document_file, owner_id)

# schedule to be run with django-q ( must be started separately. )
print('running as djangoq-tasks.')
for doc in [docu for docu in Pdf.objects.all().iterator()]:
    print(f'doc.id:{doc.id}')
    set_up_document_background_image_tasks(doc)
