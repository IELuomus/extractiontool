import os
import django

# note: it seems this kind of headless script can only be run in the django root folder
# to run: python3 example_tesseract_headless_script.py

# needed for headless script only.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # project/settings.py
django.setup()

from tesserakti.models import Word, Page, Block, Paragraph, Line
from pdf.models import Document

# dokkari = Document.objects.get(filename='Egoscue1979.pdf') # works
dokkari = Document.objects.get(id=1)
print(f"All first page words from {dokkari.filename}")
sql_page_0 = f'select * from tes_word where document_id = {dokkari.id} and page_id = 0 order by block_id, paragraph_id, line_id, word_id'
for word in Word.objects.raw(sql_page_0):
    print(word.text, end=' ')

print()
print()

dokkari = Document.objects.get(id=2)
print(f"All words from {dokkari.filename}")
sql_all = f'select * from tes_word where document_id = {dokkari.id} order by block_id, paragraph_id, line_id, word_id'
for word in Word.objects.raw(sql_all):
    print(word.text, end=' ')

print()
print()

dokkari = Document.objects.get(id=1)
print(f"All first page, first paragraph words from {dokkari.filename}")
sql_page_0_paragraph_0 = f'select * from tes_word where document_id = {dokkari.id} and page_id = 0 and paragraph_id = 0 order by block_id, paragraph_id, line_id, word_id'
for word in Word.objects.raw(sql_page_0_paragraph_0):
    print(word.text, end=' ')
