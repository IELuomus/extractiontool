ETIE database
=========

This document contains diagrams and some documentation about ETIE database schema. 

Diagrams are generated with script from an existing database.  
( `devscripts/database_diagram/create_diagrams.sh` )

Documentation is kept to a minimum, not detailing every bit.  

document
=====

Tables containing generic information about uploaded document.

Table `doc_pdf` contains basic info about the uploaded pdf-document.  

Table `doc_task` contains status information about background tasks related to the document.

Table `doc_owner` maps document and it's owner/uploader.  

( Here for clarity - table `users_user` is native to django, linked from above. )

![pdf tables](/docs/database/document_tables.png)
<!-- relative style -->
<!-- <img src="database/pdf_tables.png"> -->

information extraction
=====

Tables containing information extracted from the document.

Table `project_traittable` contains trait information extracted from the document.  

Table `table_json_table` contains information extracted from the document tables.  

Table `ner_trainer_traitnamelearndata` contains data in json format. One json object contains a field "content" with a (string) of 
the sentence content and field "annotation" with information on "text" (string of the named entity), "points" (start and end index in the sentence) and "label" (the entity label) for all NER labels, both those recognized by the spaCy nlp pipeline in spacy_parse, and those added in the annotation tool with the label 'TRAITNAME'. This data can be converted into a dataset to teach a spaCy custom named entity recognizer. 

( Here only for clarity `doc_pdf`. )  

![masterdata tables](/docs/database/ieluomus_tables.png)

tesserakti
=====

Words, Lines, Paragraphs and Blocks recognized by Tesseract OCR library.

Each of these is also linked to a single Page and Document.

Recognized regions are part of each other in the logical groups as well as coordinates.  

Order from wider to narrower is  
`tes_page` > `tes_block` > `tes_paragraph` > `tes_line` > `tes_word`.  

( Here only for clarity `doc_pdf`. )  

![tesserakti tables](/docs/database/tesseract_tables.png)

django-q task library
=====

Tables for django-q library. Django-q saves all the information about background tasks in these tables.  

Table `ieluomus_djangoq_cache_table` is created with `python manage.py createcachetables` command.

![tesserakti tables](/docs/database/djangoq_tables.png)

django native tables
=====

Here are all the tables native to django and it's basic libraries.

![tesserakti tables](/docs/database/django_tables.png)
