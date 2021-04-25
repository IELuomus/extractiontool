from document.models import Pdf, DocumentOwner
import os
from users.models import User
from django.core.files import File

# TODO: refactor and delete this file
# creates a new document to database from given pdf file and copies file under media_files/pdf/<sha1sum>/
def create_document_from_pdf_file(file_path, user_id):
        Pdf.objects.create(file=File(open(file_path, 'rb')))