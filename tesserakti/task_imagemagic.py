import os
import time
from wand.image import Image
from pdf.models import Document

class TaskImageMagick:
    taskname = ''
    document = None
    full_filepath = ''
    basename = ''
    dirname = ''
    start_path=os.getcwd()

    def __init__(self, document_id, test_path_prefix=''):
        # test_path_prefix used only in test
        self.taskname = type(self).__qualname__
        self.document = Document.objects.get(id=document_id)
        self.full_filepath = f'{test_path_prefix}{self.document.get_full_filepath()}'
        self.basename = os.path.basename(self.full_filepath)
        self.dirname = os.path.dirname(self.full_filepath)
        print(f'\nINIT {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
        os.chdir(self.start_path)

    def run(self):
        png_subdirname='page_png'
        os.makedirs(f'{self.dirname}/{png_subdirname}', exist_ok=True)
        os.chdir(self.dirname)
        print(f'STARTING {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
        for sivu in range(0,self.document.pagecount):
            new_image_filename=f'{png_subdirname}/{self.basename}-{sivu}.png'
            print(f'RUNNING {self.taskname}, create new image file: {self.dirname}/{new_image_filename}')
            with Image(filename=f'{self.basename}[{sivu}]', resolution=600) as img:
                img.save(filename=new_image_filename)
        print(f'FINISHED {self.taskname}, document.id {self.document.id}, filename: {self.basename}, pagecount: {self.document.pagecount}')
