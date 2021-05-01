import os
import time
from wand.image import Image
import pytesseract as tesse
from pytesseract import *
from document.models import Pdf
from tesserakti.models import Page, Block, Paragraph, Line, Word

class TaskTesseractOCR:
    taskname= ''
    document = None
    full_filepath = ''
    basename = ''
    dirname = ''
    start_path=os.getcwd()

    def __init__(self, document_id, test_path_prefix=''):
        # test_path_prefix used only in test
        self.taskname = type(self).__qualname__
        self.document = Pdf.objects.get(id=document_id)
        # self.full_filepath = f'{test_path_prefix}{self.document.get_full_filepath()}'
        self.full_filepath = f'{test_path_prefix}{self.document.filex.path}'
        self.basename = os.path.basename(self.full_filepath)
        self.dirname = os.path.dirname(self.full_filepath)
        os.chdir(self.start_path)
        print(f'\nINIT {self.taskname}, document.id {self.document.id}, filename: {self.basename} pagecount: {self.document.pagecount}')

    def run(self):
        print(f'STARTING {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
        png_subdirname='page_png'
        os.makedirs(f'{self.dirname}/{png_subdirname}', exist_ok=True)
        os.chdir(self.dirname)
        list_of_picture_files = ""        
        with open("picture_list.txt", "w", encoding="utf-8") as file:
            for sivu in range(0,self.document.pagecount):
                image_filename=f'{png_subdirname}/{self.basename}-{sivu}.png'
                list_of_picture_files += image_filename + "\n"
            file.write(list_of_picture_files)        
            
        pdf = tesse.image_to_pdf_or_hocr('picture_list.txt', extension='pdf')
        with open(f'OCR_{self.document.filename}', 'w+b') as f:
            f.write(pdf)

        os.remove('picture_list.txt')
        print(f'FINISHED {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
