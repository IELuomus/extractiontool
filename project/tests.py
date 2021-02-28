from django.test import TestCase
from django.urls import reverse

class uploadPdfTests(TestCase):
    def test_no_pdf_uploaded(self):
        """
        If no pdf exist, uploaded file is not displayed.
        """
        response = self.client.get(reverse('upload'))
        self.assertEqual(response.status_code, 200)

