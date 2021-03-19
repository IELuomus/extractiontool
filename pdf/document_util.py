from pdf.models import Document, DocumentOwner
import os
from users.models import User

# creates a new document to database from given pdf file and copies file under media_files/pdf/<sha1sum>/
def create_document_from_pdf_file(file_path, user_id):
        # find out sha1sum
        import subprocess
        command_result = subprocess.run(['sha1sum', f"{file_path}"], stdout=subprocess.PIPE)
        summaluku=command_result.stdout.decode('utf-8').split()[0]
        # find out filesize
        command_result = subprocess.run(['stat', '--printf=%s',f"{file_path}"], stdout=subprocess.PIPE)
        koko=int(command_result.stdout.decode('utf-8'))
        # find out pagecount
        import fitz
        pagecount=fitz.open(f'{file_path}').pageCount
        # save information about saved document to database
        newDocument = Document.objects.create(filename=f'{os.path.basename(file_path)}', size=koko, sha1sum=summaluku, pagecount=pagecount)
        DocumentOwner.objects.create(document=newDocument, owner=User.objects.get(id=user_id))
        # copy file to final location
        download_path=f'media_files/pdf/{summaluku}'
        os.makedirs(download_path, exist_ok=True)
        import shutil
        shutil.copyfile(f'{file_path}', f'{download_path}/{os.path.basename(file_path)}')
