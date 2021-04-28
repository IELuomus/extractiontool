# ETIE documentation

## Project in GitHub

[Project](https://github.com/IELuomus)

[Repository](https://github.com/IELuomus/extractiontool)

[ETIE application](https://https://etie.it.helsinki.fi/)

## Overview

The project presents the first steps towards a tool to
extract information from scientific articles into a
structured database. The application is implemented in
Python's Django together with MariaDB/MySql database. Users
are authenticated with their Orcid ID's. In its current state, 
the application offers the following functionalities:

* User can sign up and log in using Orcid ID
* User can upload a document in pdf format and application 
recognizes whether it is an image or text 
* In case of an image pdf, the application will use Tesseract 
to OCR the text from the pdf
* User can choose to extract data from tables or annotate text
* Data from tables will be saved in the database
* Annotating text will result in sentences with NER-label traitname 
to be saved into database table

## Development installation

1. Clone the project repo from https://github.com/IELuomus/extractiontool
1. Follow the instructions for [development setup](https://github.com/IELuomus/extractiontool/blob/main/docs/development_setup.md)
1. (Create local database and run `python manage.py migrate`to create the tables) included in script?
1. (Run `python manage.py createsuperuser` to create a django admin user) included in script?
1. Open 127.0.0.1:8000/admin in your browser and log in with the superuser credentials
1. Sites --> Click on example.com and edit it to refer to https://etie.it.helsinki.fi (domain) and ETIE (display)
1. Follow the instructions below to set the Orcid social application authentication

## CI/CD pipeline

### CI: GitHub Actions

### Production environment: CSC cPouta server

## Django and project structure
[Django documentation](https://docs.djangoproject.com/en/3.2/)

Main app project 
Other apps pdf, pdf_utility, tables, spacy_parse, ner_trainer

### Django admin

## Django Allauth and Orcid

### Email backend

## Uploading a pdf
Done in main app project: pdf is saved in ?
User can only see their own pdfs

## Extracting text from image
Django app pdf: Tesseract OCR

## Extracting text from a text pdf 
Django app pdf_utilities: PyMuPdf

## Extracting data from tables
Django app table: Tabula / Camelot

## Annotating text
Django apps spacy_parse and ner_trainer, frontend parse.html
### spacy_parse
The app spacy_parse first makes a .txt file of the pdf using the app pdf_utility. 
It then uses the nlp library[spaCy](spacy.io) to produce a spacy doc-object of
the text file. 

Scientific names are added to the pipe before ner from .jsonl. 

The sentences in the doc are then filtered based on a
random list of trait data words. These sentences are sent to the frontend
(parse.html).

### parse.html

### ner_trainer
