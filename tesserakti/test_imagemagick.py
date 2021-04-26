from django.test import TestCase
from document.models import Pdf
from tesserakti.models import Page, Block, Paragraph, Line, Word
import os
import requests
from tesserakti.task_imagemagic import TaskImageMagick # ok
from tesserakti.test_base import BaseTestCase
from django.test import tag

# python3 manage.py test tesserakti.test_imagemagick

class ImageMagickTestCase(BaseTestCase, TestCase):

    # def setUp(self): # defined in baseclass

    @tag('slow')
    def test_task_imagemajick(self):
        """Imagemagick task executes correctly"""

        super().base_task_imagemajick()
        os.chdir(self.start_path)
        firstfile=f'{self.download_path}/page_png/{self.filename}-0.png'
        self.assertTrue(os.path.isfile(firstfile), f'File {firstfile} created by imagemagick exists.')
