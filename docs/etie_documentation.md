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
* Annotating text will result in sentences with a new NER-label 'traitname' being saved into the database, 
  to serve as learning data in the future

## Use guidelines in wiki 

## Development installation

1. Clone the project repo from https://github.com/IELuomus/extractiontool.
1. Follow the instructions for [docker setup](https://github.com/IELuomus/extractiontool/blob/main/docs/development_setup_docker.md) using a script and an .env file. This is the recommended way to develop as all developers get the exact same target environment and there will be no problems with cross-platform compatibility.  
( NOTE: M1/Arm CPUs don't seem to work with Docker and this app, at least for now. )

1. Or follow the instructions for [development setup](https://github.com/IELuomus/extractiontool/blob/main/docs/development_setup_using_scripts.md) using a bash script and an .env file.
1. Or follow [these](https://github.com/IELuomus/extractiontool/blob/main/docs/development_setup_manual.md) instructions to set everything up manually. 

## Run the app locally

1. Run `python manage.py runsslserver`. The sslserver is required by the Orcid login (see below).
1. Open browser at https://127.0.0.1:8000. Disregard the warning about a missing certificate and find the proper way to bypass this,
depending on your browser

1. Login at https://127.0.0.1:8000/admin with your superuser credentials to inspect Django admin panel, with e.g. the possibility to see and edit
database tables. In order to see the tables there, they tables must be registered in the admin.py file of the respective app. 

## CI/CD pipeline

### CI: GitHub Actions
Continuous integration is implemented by GitHub Actions. There are two sets of tests: [Development testing](https://github.com/IELuomus/extractiontool/actions/runs/830148389/workflow) and [Django CI](https://github.com/IELuomus/extractiontool/actions/runs/828076067/workflow). Development testing doesn't have (m)any tests. 

### Docker

[Docker guidelines](https://github.com/IELuomus/extractiontool/blob/main/docs/Docker.md)

### Production environment: CSC cPouta server


## Django and project structure

[Architecture overview](https://github.com/IELuomus/extractiontool/blob/main/docs/architecture_overview.md)
[Directory structure overview](https://github.com/IELuomus/extractiontool/blob/main/docs/directory_structure_overview.md)

Django applications are structured using several 'django apps', each of which is responsible for (ideally) one functionality. The apps are in separate folders with their own models.py (models for database tables), urls.py (ursl for direction of requests) and views.py (functionality) files. The 'main app' contains django's settings in the settings.py file. In the ETIE application the main app is called simply 'project'. The urls.py file in the 'project' folder contains references to all the other apps' urls.py files so that requests can be directed to the correct url-addresses.  

See also [Django documentation](https://docs.djangoproject.com/en/3.2/)

Other django apps are document, table, spacy_parse, ner_trainer, and tesserakti. All of these apps must be listed in settings.py INSTALLED_APPS list to be functional. In addition, the folder "users" contains the models and urls for user authentication. This implementation overrides Django's default user handling and is required by the Orcid social authentication. Other folders are "features" (templates for feature tests), "devscripts" (scripts for development setup), "docker" (docker files), "docs" (documentation), "static" (javascript files), "static_templates" (also javascript files?), "templates" (html templates), LOGS(?), CONF(?). 

Other files:
The (large) file patterns_scientificNames.jsonl contains in json format all names of mammals (both present and fossile) and the associated NER label SCIENTIFICNAME. This file is used in spacy_parse/views.py as a source whereform they the names and labels are read into the entity ruler in the spaCy pipeline (see below Annotating text).

## Django Allauth and Orcid
User identification in the ETIE application happens with the [Django Allauth library](https://django-allauth.readthedocs.io/) and social account provider [Orcid](https://orcid.org). Orcid id's are unique identifiers used by researchers and other people in the academia. When the user clicks on the orcid-button in ETIE log in screen, they are directed to the log in page at orcid.org. After entering their Orcid credentials, if they are already registered users of ETIE application, they will be redirected to the ETIE front page with "logged in" status; otherwise, they will be redirected to a page in ETIE where they are prompted to enter their email for registration and verification (note that you can't use the email used in Django admin (superuser) to login with Orcid).

### Orcid configuration
The Orcid configuration contains the site address of the application together with callback urls for both production environment and local development. These need to be in https form. First create an Orcid id, login, and from the upper right corner under your account info go to 
"developer tools". Here set the callback urls. 

### Email backend
Email backend is needed to send the verification email to new users of ETIE application. The username and password for the email backend are defined in the .env file. Email host is now set as gmail.com (`EMAIL_HOST = "smtp.gmail.com"` in project/settings.py where also other email backend settings can be found and adjusted). Note that for the gmail backend to work you will need to set the security settings of the email account to allow access to potentially harmful sites.

## Uploading a pdf
Done in main app project: pdf is saved in the media folder.
User can only see their own pdfs

## Extracting text from an image pdf
Django app tesserakti: Tesseract OCR
Workers: django-q

When a user uploads a document, tasks are started in the background:  
1. Generate `.png` -images of each page to `png_page/` folder in the document upload folder using ImageMagick-library.
2. Generate `OCR_<original_filename>` by combining `.png` images and text recognized from them. Resulting in a new pdf file which has searchable text even if the original format was picture-based.
3. From the `.png`-page-images, Tesseract-recognized words, lines, paragraphs and blocks are saved to database, each linked to specific document and page.  

Note: All these tasks are currently done for all uploaded documents.  

## Extracting text from a text pdf 
Django app "document": PyMuPdf

## Extracting data from tables
Django app "table", together with frontend template selected_tables.html.
Camelot, a Python library for extracting tables from PDF files, is used to extract tables from PDF files with page number as a parameter.

When a user feeds the page number, the program both displays the extracted tables for the user as well as stores them in a database table called "Table_Json_Table". Json_Table contains the following fields: "user_id", "pdf_id", "page_number", "table_num" (the number of a specific table on a given page), "json_table" (the table in json format), "table" (the file path for the json file of a given table). 

A user can select the following values from the selected table(s):
 "verbatimTraitName", "verbatimTraitValue", "verbatimTraitUnit", "sex", and "verbatimScientificName."
After the selection, a user can store the selected values in the "Project_TraitTable" database table.

## Annotating text
Django apps "spacy_parse" and "ner_trainer", together with frontend template parse.html. These three components produce sentences in json format containing annotations for a new ner label 'traitname'. The sentences are stored in the database (table TraitnameLearnData), and the purpose is to use them to train a ner model to recognize ecological trait names (e.g. body weight, tail length, diet) in scientific articles on mammalian data.

### spacy_parse
The method spacy_parse/views.py/parse first calls document.pdf_reader/pdf_to_text function to render the pdf text as a .txt file. The output string is then submitted to a linguistic analysis using the [spaCy](spacy.io) NLP library. SpaCy offers several different [trained models](https://spacy.io/models) for English. The packages can be directly downloaded in python code. The package used at the moment is en_core_web_lg   `spacy.load("en_core_web_lg")`.
 
 The following command produces a spaCy doc-object with tokenization, lemmatization, sentencizer, and named entity recognition of the input string.
 
 `doc = nlp(text)`

The sentences in the doc object are then filtered based on a more or less random list of potential trait data words. 
This is to avoid going through all the sentences in the document in the annotating phase. 

A new string string (trait_text) is compiled from these sentences, and another doc-object is created:

`trait_doc = nlp(trait_text)`

Before that, certain modifications are done in the spaCy pipeline. 

Named entities and noun_chunks (i.e. noun phrases) are merged so that entities consisting of more than one word/token are properly recognized.

`nlp.add_pipe("merge_entities")
 nlp.add_pipe("merge_noun_chunks")`

Next, scientific names of mammals are added to the pipeline as an entity ruler (rule-based recognition) from a .jsonl file:

`ruler = nlp.add_pipe("entity_ruler", before="ner").from_disk(
            "./patterns_scientificNames.jsonl")`

Before="ner" in the above means that the entity ruler is applied in the pipeline before the statistical ner recognition enabled by the trained model takes place.

Next the sentences are converted into python dicts (see [these guidelines](https://towardsdatascience.com/custom-named-entity-recognition-using-spacy-7140ebbb3718)) containing all existing NER labels. The dicts are converted into json and sent to the frontend (parse.html) for annotation.

### parse.html and ner_trainer

The sentences are parsed into native json-objects and their content is shown to the user one by one. The selected text is added to the json-object's annotation list with label "TRAITNAME", and the sentence is sent further to the backend ner_trainer where the json is saved into the database table TraitnameLearnData.


