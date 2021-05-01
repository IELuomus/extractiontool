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

def imagemagic_task_run(dokkari_id):
    task_imagemagick = TaskImageMagick(dokkari_id)
    task_imagemagick.run()

def tesseract_task_run(dokkari_id):
    task = TaskTesseract(dokkari_id)
    task.run()

def tesseract_task_OCR_run(dokkari_id):
    task = TaskTesseractOCR(dokkari_id)
    task.run()


if len(sys.argv) > 1 and sys.argv[1] == 'old':
    q = 'no'
else:
    q = 'yes'

print("Number of processors: ", mp.cpu_count())

# to make things easier delete everything..
for malli in (DocumentTask, DocumentOwner, Word, Line, Paragraph, Block, Page, Pdf):
    # this delete is slow?
    # malli.objects.all().delete()
    # delete fast(?)
    queryset = malli.objects.all()
    queryset._raw_delete(queryset.db)

# tiedostojen_polku='../all_testfiles/'
tiedostojen_polku='../some_testfiles'

# create documents to database ( and copy under media/pdf/<sha1sum>/ )
for document_file in Path(tiedostojen_polku).glob("**/*.pdf"):
    owner_id=1
    create_document_from_pdf_file(document_file, owner_id)

if q == 'yes':
    print('running as djangoq-tasks.')
    for doc in [docu for docu in Pdf.objects.all().iterator()]:
        print(f'doc.id:{doc.id}')
        set_up_document_background_image_tasks(doc)
    print("ALL GOOD.")

else:
    # old style

    # run imagemagick-task for all documents in parallel
    all_documents = Pdf.objects.all().iterator()
    pool = mp.Pool(mp.cpu_count())
    pool.map(imagemagic_task_run, [docu.id for docu in all_documents])
    pool.close()

    # run tesseract-OCR-task for all documents in parallel
    all_documents = Pdf.objects.all().iterator()
    pool2 = mp.Pool(mp.cpu_count())
    pool2.map(tesseract_task_OCR_run, [docu.id for docu in all_documents])
    pool2.close()    

    # run tesseract-task for all documents in parallel
    all_documents = Pdf.objects.all().iterator()
    pool2 = mp.Pool(mp.cpu_count())
    pool2.map(tesseract_task_run, [docu.id for docu in all_documents])
    pool2.close()    

