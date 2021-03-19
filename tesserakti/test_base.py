from django.test import TestCase
from pdf.models import Document
from tesserakti.models import Page, Block, Paragraph, Line, Word
import os
import requests
from tesserakti.task_imagemagic import TaskImageMagick # ok
import time

# inherit from object, 'abstract' testcase. these wont run withouth subclass implementation.
class BaseTestCase(object):

    download_path = ''
    filename = ''
    start_path=os.getcwd()
    temp_root_dir = ''

    def setUp(self):
        self.temp_root_dir = f'temp_tesserakti_tests_{round(time.time() * 1000)}/'
        # download and write to temp-dir
        os.makedirs(self.temp_root_dir, exist_ok=True)
        
        # 3 sivua
        self.filename='58897-Article Text-58966-1-10-20101216-1.pdf'
        url_pdf='https://journals.flvc.org/flaent/article/download/58897/56576'
        
        # 16 sivua
        # self.filename='y0870e67.pdf'
        # url_pdf=f'http://www.fao.org/3/y0870e/{self.filename}'

        # download to temp dir
        response = requests.get(url_pdf, allow_redirects=True)
        open(f'{self.temp_root_dir}/{self.filename}', 'wb').write(response.content) # wb=write binary
        # find out sha1sum
        import subprocess
        command_result = subprocess.run(['sha1sum', f"{self.temp_root_dir}/{self.filename}"], stdout=subprocess.PIPE)
        summaluku=command_result.stdout.decode('utf-8').split()[0]
        # find out filesize
        command_result = subprocess.run(['stat', '--printf=%s',f"{self.temp_root_dir}/{self.filename}"], stdout=subprocess.PIPE)
        koko=int(command_result.stdout.decode('utf-8'))
        # find out pagecount
        import fitz
        pagecount=fitz.open(f'{self.temp_root_dir}/{self.filename}').pageCount

        # save information about saved document to database
        Document.objects.create(filename=f'{self.filename}', size=koko, sha1sum=summaluku, pagecount=pagecount)
        # move file to final location
        self.download_path=f'{self.temp_root_dir}/media_files/pdf/{summaluku}'
        os.makedirs(self.download_path, exist_ok=True)
        os.rename(f'{self.temp_root_dir}/{self.filename}', f'{self.download_path}/{self.filename}')

    def tearDown(self):
        # delete downloaded pdf-file, generated .png files and temp dirs
        os.chdir(self.start_path)
        os.remove(f'{self.download_path}/{self.filename}')
        from pathlib import Path
        for png_file in Path(f'{self.download_path}/page_png').glob("*.png"):
            png_file.unlink()
        os.rmdir(f'{self.download_path}/page_png')
        os.rmdir(self.download_path)
        os.rmdir(f'{self.temp_root_dir}/media_files/pdf')
        os.rmdir(f'{self.temp_root_dir}/media_files')
        os.rmdir(f'{self.temp_root_dir}')

    def base_task_imagemajick(self):
        dokkari = Document.objects.first()
        task_imagemagick = TaskImageMagick(dokkari.id, self.temp_root_dir)
        task_imagemagick.run()
