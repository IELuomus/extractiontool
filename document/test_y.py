from django.test import TestCase
from document.models import Pdf
import os

# python3 manage.py test pdf.test_x

# dummy test testing running test
class PdfTestCase(TestCase):

    def test_task_imagemajick(self):
        """Pdf test x"""

        message="THIS IS A TEST - THIS HAS HAPPENED BEFORE"
        print(f'{message}.')
        # no comment

        self.assertTrue(message != "incomprehensible", f'Message is {message}.')
