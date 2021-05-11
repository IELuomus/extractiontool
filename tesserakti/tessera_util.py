from document.models import Pdf, DocumentTask
from tesserakti.task_imagemagic import TaskImageMagick
from tesserakti.task_tesseract import TaskTesseract
from tesserakti.task_tesseract_OCR import TaskTesseractOCR
from django_q.tasks import async_task, schedule
import os
import shutil
from tesserakti.models import Word, Page, Block, Paragraph, Line
from django.core.exceptions import ObjectDoesNotExist

def set_up_document_background_image_tasks(pdf_document):

    print(f'creating background image tasks for document id {pdf_document.id}')

    DocumentTask.objects.create(
        document=pdf_document, 
        name=DocumentTask.DocTaskName.IMAGEMAGICK,
        status=DocumentTask.DocTaskStatus.WAITING)

    DocumentTask.objects.create(
        document=pdf_document, 
        name=DocumentTask.DocTaskName.TESSERACT_OCR,
        status=DocumentTask.DocTaskStatus.WAITING)

    DocumentTask.objects.create(
        document=pdf_document, 
        name=DocumentTask.DocTaskName.TESSERACT_DB,
        status=DocumentTask.DocTaskStatus.WAITING)

    async_task('tesserakti.tessera_util.document_background_image_tasks', pdf_document.id)

def document_background_image_tasks(document_id):

    print(f'starting document_background_image_tasks for document id={document_id}')

    document = Pdf.objects.get(id=document_id)

    # get statuses and act accordingly in case task failed. ( server went down or something unexpected. )
    imagemagic_task_status = DocumentTask.objects.raw(f'select id, document_id, name, status, time from doc_task where document_id = {document.id} and name = "{DocumentTask.DocTaskName.IMAGEMAGICK}" order by time desc limit 1;')
    tesseract_ocr_pdf_task_status = DocumentTask.objects.raw(f'select id, document_id, name, status, time from doc_task where document_id = {document.id} and name = "{DocumentTask.DocTaskName.TESSERACT_OCR}" order by time desc limit 1;')
    tesseract_db_task_status = DocumentTask.objects.raw(f'select id, document_id, name, status, time from doc_task where document_id = {document.id} and name = "{DocumentTask.DocTaskName.TESSERACT_DB}" order by time desc limit 1;')

    # imagemagick
    if ( imagemagic_task_status != DocumentTask.DocTaskStatus.FINISHED):
        if ( imagemagic_task_status != DocumentTask.DocTaskStatus.WAITING):
            print(f'{DocumentTask.DocTaskName.IMAGEMAGICK} task with document id {document.id} cleaning up previous unfinished run.')
            try:
                if document.filex:
                    path = f'media/{os.path.dirname(str(document.filex))}/page_png'
                    shutil.rmtree(path) # delete directory including all it's contents
            except:
                pass

        DocumentTask.objects.create(
            document=document, 
            name=DocumentTask.DocTaskName.IMAGEMAGICK,
            status=DocumentTask.DocTaskStatus.RUNNING)

        task_imagemagick = TaskImageMagick(document.id)
        task_imagemagick.run()    

        DocumentTask.objects.create(
            document=document, 
            name=DocumentTask.DocTaskName.IMAGEMAGICK,
            status=DocumentTask.DocTaskStatus.FINISHED)

    # tesseract ocr
    if (tesseract_ocr_pdf_task_status != DocumentTask.DocTaskStatus.FINISHED):
        if ( tesseract_ocr_pdf_task_status != DocumentTask.DocTaskStatus.WAITING):
            print(f'{DocumentTask.DocTaskName.TESSERACT_OCR} task with document id {document.id} cleaning up previous unfinished run.')
            try:
                os.remove(f'OCR_{document.filename}')
            except:
                pass

        DocumentTask.objects.create(
            document=document, 
            name=DocumentTask.DocTaskName.TESSERACT_OCR,
            status=DocumentTask.DocTaskStatus.RUNNING)

        task_tesseract_OCR = TaskTesseractOCR(document.id)
        task_tesseract_OCR.run()    

        DocumentTask.objects.create(
            document=document, 
            name=DocumentTask.DocTaskName.TESSERACT_OCR,
            status=DocumentTask.DocTaskStatus.FINISHED)

    # tesseract db
    if (tesseract_db_task_status != DocumentTask.DocTaskStatus.FINISHED):
        if ( tesseract_db_task_status != DocumentTask.DocTaskStatus.WAITING):
            print(f'{DocumentTask.DocTaskName.TESSERACT_DB} task with document id {document.id} cleaning up previous unfinished run.')
            for malli in (Word, Line, Paragraph, Block, Page):
                try:
                    queryset = malli.objects.filter(document_id=document.pk)
                    queryset._raw_delete(queryset.db)
                except ObjectDoesNotExist:
                    pass

        DocumentTask.objects.create(
            document=document, 
            name=DocumentTask.DocTaskName.TESSERACT_DB,
            status=DocumentTask.DocTaskStatus.RUNNING)

        task_tesseract_db = TaskTesseract(document.id)
        task_tesseract_db.run()

        DocumentTask.objects.create(
            document=document, 
            name=DocumentTask.DocTaskName.TESSERACT_DB,
            status=DocumentTask.DocTaskStatus.FINISHED)

    print(f'finished document_background_image_tasks for document id={document_id}')
