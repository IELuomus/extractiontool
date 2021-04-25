from django.test import TestCase
from document.models import Pdf
from tesserakti.models import Page, Block, Paragraph, Line, Word
import os
import requests
from tesserakti.test_base import BaseTestCase
from tesserakti.task_tesseract import TaskTesseract
from django.test import tag

# python3 manage.py test tesserakti.test_tesseract

class TesseractTestCase(BaseTestCase, TestCase):
    def setUp(self):
        super().setUp()
        super().base_task_imagemajick()

    @tag('slow')
    def test_task_tesseract(self):
        """Tesseract task executes correctly"""

        dokkari = Pdf.objects.first()
        task = TaskTesseract(dokkari.id, self.temp_root_dir)
        task.run()
        sivuja=Page.objects.all().count()
        self.assertTrue(sivuja == dokkari.pagecount, f'document with name {dokkari.filename} was inserted into database with {dokkari.pagecount} pages.')
