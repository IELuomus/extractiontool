# ETIE documentation

[ETIE application](https://etie.it.helsinki.fi/)

## Project in GitHub

[Project](https://github.com/IELuomus)

[Repository](https://github.com/IELuomus/extractiontool)

## Overview

The project presents the first steps towards a tool to
extract information from scientific articles into a
structured database. The application is implemented in
Python's Django together with MariaDB/MySql database. Users
are authenticated with their Orcid ID's. In its current state, 
the application offers the following functionalities:

* User can sign up and log in using an Orcid ID
* User can upload a document in pdf format and the application 
recognizes whether it is an image or text 
* In case of an image pdf, the application will use Tesseract 
to OCR the text from the pdf
* When the pdf is in text format, the user can choose to either extract data from tables or annotate text
* Data extracted from tables will be saved in the database as ecological trait data
* Annotating text will result in sentences with a new NER-label 'traitname' being saved into the database

## Use guidelines in wiki 

## Development installation

1. Clone the project repo from https://github.com/IELuomus/extractiontool.
1. Follow the instructions for [development setup](https://github.com/IELuomus/extractiontool/blob/main/docs/development_setup.md) using a bash script and an .env file.
1. Or follow these (forthcoming) instructions to set everything up manually. 
1. Run `python manage.py runsslserver`
1. Open https://127.0.0.1:8000/ in your browser. The browser will most likely complain about the missing certificate, but this can just be ignored.


## CI/CD pipeline

### CI: GitHub Actions
Continuous integration is implemented by GitHub Actions. There are two sets of tests: Development testing and Django CI. Development testing doesn't have (m)any tests. 

### Production environment: CSC cPouta server


## Django and project structure
[Django documentation](https://docs.djangoproject.com/en/3.2/)

Django applications are structured using several 'django apps', each of which is responsible for (ideally) one functionality. The apps are in separate folders with their own models.py, urls.py and views.py files. The 'main app' contains django's settings in the settings.py file. In the ETIE application the main app is called simply 'project'. The urls.py file in the 'project' folder contains references to all the other apps' urls.py files.  

Other django apps are document, table, spacy_parse, ner_trainer, and tesserakti. All apps must be listed in settings.py INSTALLED_APPS list. In addition, the folder users contains the models and urls for user authentication.

All html templates are currently in the templates folder.

### Django admin

Go to https://127.0.0.1:8000/admin to log in with the superuser credentials (as defined in the .env file).

## Django Allauth and Orcid
User identification in ETIE applications happens with the [Django Allauth library](https://django-allauth.readthedocs.io/) and social account provider [Orcid](https://orcid.org). Orcid id's are unique identifiers used by researchers and other people in academia. When the user clicks on the orcid-button in ETIE log in screen, they are directed to the log in page of orcid.org. If they are already registered users of ETIE application, they will be redirected to the ETIE front page; otherwise, they will be redirected to a page in ETIE where they are prompted to enter their email for registration and verification (??what happens if it is not the same email?).

### Orcid configuration
The orcid configuration contains the site address of the application together with callback urls for both production environment and local development. These need to be in https form. 

### Email backend
Email backend is needed to send the verification email to new users of ETIE application. The username and password are defined in the .env file. Email host is now set as gmail.com (`EMAIL_HOST = "smtp.gmail.com"` in project/settings.py where also other email backend settings can be found and adjusted).

## Uploading a pdf
Done in main app project: pdf is saved in the media folder.
User can only see their own pdfs

## Extracting text from an image pdf
Django app pdf: Tesseract OCR
Workers: django-q

## Extracting text from a text pdf 
Django app pdf_utilities: PyMuPdf

## Extracting data from tables
Camelot, a Python library for extracting tables from PDF files, is used to extract tables from PDF files with page number as a parameter.
Django app table, frontend selected_tables.html

A user can select the following values from the selected table(s):
 "verbatimTraitName", "verbatimTraitValue", "verbatimTraitUnit", "sex", and "verbatimScientificName."
After the selection, a user can store the selected values in the "TraitTable" database table.

## Annotating text
Django apps spacy_parse and ner_trainer, frontend parse.html. The components produce sentences in json form conatining annotations for a new ner label 'traitname'. The sentences are stored in database, and the purpose is to use them to train a ner model to recognize ecological trait names (e.g. body weight, tail length, diet) in scientific articles on mammalian data.

### spacy_parse
The method spacy_parse/views.py/parse first calls document.pdf_reader/pdf_to_text function to render the pdf text as a .txt file. The output string is then submitted to a linguistic analysis using the [spaCy](spacy.io) NLP library. SpaCy offers several different [trained models](https://spacy.io/models) for English. The packages can be directly downloaded in python code. The package used at the moment is en_core_web_lg   `spacy.load("en_core_web_lg")`.
 
 The following command produces a spaCy doc-object with tokenization, lemmatization, sentencizer, and named entity recognition of the input string.
 
 `doc = nlp(text)`

Before that, certain modifications are done in the spaCy pipeline. 

Named entities and noun_chunks (i.e. noun phrases) are merged so that entities consisting of more than one word/token are properly recognized.

`nlp.add_pipe("merge_entities")
 nlp.add_pipe("merge_noun_chunks")`

Next, scientific names of mammals are added to the pipeline as an entity ruler (rule-based recognition) from a .jsonl file:

`ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk(
            "./patterns_scientificNames.jsonl")`

Before="ner" in the above means that the entity ruler is applied in the pipeline before the statistical ner recognition enabled by the trained model takes place.

The sentences in the doc are then filtered based on a
more or less random list of potential trait data words. This is to avoid going through all the sentences in the document in the annotating phase. Another string is compiled from these sentences, and another doc-object is rendered (??Oikeastaan scientific names pitäisi tulla vasta tässä?). These sentences are sent to the frontend (parse.html) for annotation.

### parse.html

### ner_trainer
