from django.test import TestCase
from pdf.models import Document
import os

# python3 manage.py test pdf.test_x

# dummy test testing running test
class PdfTestCase(TestCase):

    def test_task_imagemajick(self):
        """Pdf test x"""

        message="HELLOU"
        print(f'{message}!!!')
        # no comment

        self.assertTrue(message == "HELLOU", f'Message is {message}.')
