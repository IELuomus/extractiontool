import os
import time
from wand.image import Image
import pytesseract as tesse
from pytesseract import*
from document.models import Pdf
from tesserakti.models import Page, Block, Paragraph, Line, Word

class TaskTesseract:
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
        self.full_filepath = f'{test_path_prefix}{self.document.file.path}'
        self.basename = os.path.basename(self.full_filepath)
        self.dirname = os.path.dirname(self.full_filepath)
        os.chdir(self.start_path)
        print(f'\nINIT {self.taskname}, document.id {self.document.id}, filename: {self.basename} pagecount: {self.document.pagecount}')

    def run(self):
        print(f'STARTING {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
        png_subdirname='page_png'
        os.makedirs(f'{self.dirname}/{png_subdirname}', exist_ok=True)
        os.chdir(self.dirname)
        for sivu in range(0,self.document.pagecount):
            image_filename=f'{png_subdirname}/{self.basename}-{sivu}.png'
            print(f'RUNNING {self.taskname}, process image file: {self.dirname}/{image_filename}')
            data=tesse.image_to_data(image_filename, output_type=Output.DATAFRAME, config="--dpi 600 -l eng")
            data.fillna(value="", inplace=True)
            for row in data.itertuples(index = True, name ='Area'): 
                tyyppi=row.level
                if (tyyppi == 1):
                    Page.objects.create(page_id=sivu, document_id=self.document.id, vasen=row.left, top=row.top, width=row.width, height=row.height)
                if (tyyppi == 2):
                    Block.objects.create(block_id=row.block_num, page_id=sivu, document_id=self.document.id, vasen=row.left, top=row.top, width=row.width, height=row.height)
                if (tyyppi == 3):
                    Paragraph.objects.create(paragraph_id=row.par_num, block_id=row.block_num, page_id=sivu, document_id=self.document.id, vasen=row.left, top=row.top, width=row.width, height=row.height)
                if (tyyppi == 4):
                    Line.objects.create(line_id=row.line_num, paragraph_id=row.par_num, block_id=row.block_num, page_id=sivu, document_id=self.document.id, vasen=row.left, top=row.top, width=row.width, height=row.height)
                if (tyyppi == 5):
                    Word.objects.create(text=row.text, conf=row.conf, word_id=row.word_num, line_id=row.line_num, paragraph_id=row.par_num, block_id=row.block_num, page_id=sivu, document_id=self.document.id, vasen=row.left, top=row.top, width=row.width, height=row.height)
        print(f'FINISHED {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
