import os
import django
# needed for headless script only.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # project/settings.py
django.setup()
from tesserakti.models import Word, Page, Block, Paragraph, Line
from pdf.models import Document
from pdf.document_util import *
import multiprocessing as mp
from tesserakti.task_imagemagic import TaskImageMagick
from tesserakti.task_tesseract import TaskTesseract

print("Number of processors: ", mp.cpu_count())

def imagemagic_task_run(dokkari):
    task_imagemagick = TaskImageMagick(dokkari.id)
    task_imagemagick.run()

def tesseract_task_run(dokkari):
    task = TaskTesseract(dokkari.id)
    task.run()

# to make things easier delete everything..
# for malli in (DocumentOwner, Document, Word, Line, Paragraph, Block, Page):
#     malli.objects.all().delete()

# tiedostojen_polku='../all_testfiles/'
tiedostojen_polku='../some_testfiles'

# create documents to database and copy under media_files/pdf/<sha1sum>/
from pathlib import Path
for document_file in Path(tiedostojen_polku).glob("**/*.pdf"):
    owner_id=1
    create_document_from_pdf_file(document_file, owner_id)

# run imagemagick-task for all documents in parallel
all_documents = Document.objects.all().iterator()
pool = mp.Pool(mp.cpu_count())
pool.map(imagemagic_task_run, [docu for docu in all_documents])
pool.close()

# run tesseract-task for all documents in parallel
all_documents = Document.objects.all().iterator()
pool2 = mp.Pool(mp.cpu_count())
pool2.map(tesseract_task_run, [docu for docu in all_documents])
pool2.close()    
