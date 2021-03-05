from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile


# class uploadPdfTests(TestCase):

#     def test_no_pdf_uploaded(self):
#         """
#         If no pdf exist, uploaded file is not displayed.
#         """
#         response = self.client.get(reverse('upload'))
#         self.assertEqual(response.status_code, 200)


#     def test_upload_video(self):
#         document = SimpleUploadedFile("file.pdf", b"file_content", content_type="pdf")
#         self.client.post(reverse('upload'), {'document': document})
#         self.assertTemplateUsed('upload.html')