from document.models import Pdf, DocumentTask
from tesserakti.task_imagemagic import TaskImageMagick
from tesserakti.task_tesseract import TaskTesseract
from tesserakti.task_tesseract_OCR import TaskTesseractOCR
from django_q.tasks import async_task, schedule

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

    # imagemagick
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
