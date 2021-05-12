
*Quick overview of the Architecture*

**Structure**

Django main app and submodules (ie. apps in the Django-lingo).

Our main application folder is  
> `project`  

Submodules are  
>> `document`  uploaded document    
>> `ner_trainer` NER trainer    
>> `spacy_parse` SpaCy parse    
>> `table` table parsing    
>> `tesserakti` Tesseract OCR  
>> `users` overriden Django-User-model

Sub-modules should, in principle, contain functionality which can be thought of as independent and separate from the main application (like third party libraries, extendable and overridable). The main application should depend on the submodules, but never the other way. The main application should have all the functionality which can be thought of as specific to that application.  

Note: In this project these principles don't always hold true for historical reasons (all were Django-newbies).  


**Runtimes**  

***Main Server***  

Development:  
> `python manage.py sslserver`

Production:
> `gunicorn --bind 0.0.0.0:443 ...`
  
***Background Tasks***  
Development & Production:  
> `python manage.py qcluster`

Background tasks communicate with the main app only through the database. ( Although django-q does have hooks which could call same code, but this is not used. )






