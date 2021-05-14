# example script how to query words from database from documents which were uploaded and words recognized with Tesseract OCR library.

# to run: python3 example_tesseract_headless_script.py
import os
import django
# needed for headless script only.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # project/settings.py
django.setup()
from tesserakti.models import Word, Page, Block, Paragraph, Line
from document.models import Pdf

try:
    # dokkari = Pdf.objects.get(filename='39_Geiser_2009.pdf') # works
    dokkari = Pdf.objects.get(id=1) # works
    # dokkari = Pdf.objects.all()[0]
    print(f"All first page words from {dokkari.filename}")
    sql_page_0 = f'select * from tes_word where document_id = {dokkari.id} and page_id = 1 order by block_id, paragraph_id, line_id, word_id'
    for word in Word.objects.raw(sql_page_0):
        print(word.text, end=' ')

    print()
    print()

    dokkari = Pdf.objects.all()[1]
    print(f"All words from {dokkari.filename}")
    sql_all = f'select * from tes_word where document_id = {dokkari.id} order by block_id, paragraph_id, line_id, word_id'
    for word in Word.objects.raw(sql_all):
        print(word.text, end=' ')

    print()
    print()

    dokkari = Pdf.objects.all()[0]
    print(f"All first page, first paragraph words from {dokkari.filename}")
    sql_page_0_paragraph_0 = f'select * from tes_word where document_id = {dokkari.id} and page_id = 0 and paragraph_id = 0 order by block_id, paragraph_id, line_id, word_id'
    for word in Word.objects.raw(sql_page_0_paragraph_0):
        print(word.text, end=' ')

except:
    print('pass')
    pass