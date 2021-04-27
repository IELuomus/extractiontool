from document.models import Pdf, DocumentOwner
from tesserakti.task_imagemagic import TaskImageMagick
from tesserakti.task_tesseract import TaskTesseract

def imagemagic_task_run(dokkari_id):
    task_imagemagick = TaskImageMagick(dokkari_id)
    task_imagemagick.run()

def tesseract_task_run(dokkari_id):
    task = TaskTesseract(dokkari_id)
    task.run()
