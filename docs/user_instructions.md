# ETIE User Guide

## Logging in and creating an account

You can log in to ETIE at https://etie.it.helsinki.fi/ and choosing "Log in | Sign up"

You can log in with either your username and password, or with your ORCID, if you click the orcid-button.

You can create a new user account at https://etie.it.helsinki.fi/accounts/signup/

## Uploading a file

After logging in, you are taken to the Pdfs -view where you can upload a pdf -file to ETIE or start processing a file. Click the "Upload pdf" -button and you can upload a pdf.

Upload pdf asks you several key bits of info of the pdf that you're going to upload, as follows:

**Required fields:**
- Title - This is the title of the article or the book that you're going to be downloading.
- Author - This is the author or authors of the article or book. It is recommended to use the same convention as in the article or book itself.

**Optional fields:**
- Journal - The publication where the article was published
- Volume - The number or name of the volume where the article was published, or the number of the volume in series of books
- Issue - The specific issue of the journal where the article was published
- Pages - The page numbers of the article in the issue where it was published
- Year - The year when the article or book was published
- Publisher - The publisher of the article or book.
  
After filling in the fields above, click Choose file, and a file browser will open up, choose the correct file and click Open.

Finally, click Upload pdf at the bottom of the page.

## Processing a file

After uploading a file, you can choose to either extract data from tables, or annotate text. Click either Extrat Data from Tables or Annotate Text -button next to the file you wish to process.

### Annotate text

To start annotating a text, click Annotate text -button next to the pdf you want to start annotating. For now this process will take some time to start due to the server-side issues, so some patience is required.

After some time, you will be shown a page with the first potential sentence containing trait data in the uploaded document. You can then choose a word (or several words) that should be annotated with the named entity label “TRAITNAME”, and by clicking “Select a traitname” the selected words will appear in the window. When “Confirm selection” is clicked, the sentence with the new annotation will be saved in the database.

The purpose of this functionality is to produce learning data to train a custom named entity model, eventually to be included in the spaCy pipeline. 

**The annotated text is not saved into the database at the moment.

### Extract data from tables

**Quick-start Guide**
  1) Hilight and then click one of the Get-buttons. Repeat as needed, getting the species name, the relevant trait, and the trait value
  2) Select trait unit and sex of the animal
  3) Click the Post-button to add the new entry into the Traitdata database

In this view first enter a page number from the pdf that contains a table and then click OK. You will then be forwarded to a new view where you can manually extract data from the table in question. Here you have several options, for each option first highlight the text in question from the table, and then click one of the buttons above the table.

**Get Buttons:**
- Get Trait Name - The highlighted text is specified as the trait name
- Get Trait Value - The highlighted text is specified as the trait value for the chosen trait name
- Get Scientific Name Value - The highlighted text is specified as the scientific name for the species of animal that the trait regards
  
**Note** For each of these buttons, you can either highlight the text from the table below, or type in the word if it doesn't appear in the table (for instance, if the scinetific name of the animal is not included in the table.)
  
**Select dropdown boxes:**
- Select trait unit - You can choose the correct unit for the trait from this dropdown box, the default is "not speficied"
- Select sex for the species - You can choose the sex of the animal whom the trait is measured for, the default is "not specified"

**Post-button**
- After you have filled all the other fields, click the Post-button to add a new entry to the trait-data database.

## My pdfs -view

Clicking the My pdfs button takes the user to the Pdfs view that shows all the pdfs that the user has uploaded to the service. From here the user can also upload another pdf to the service, and see the status of the pdfs that they have already downloaded.

### Pdfs

On the first table, there user can see the pdf files that they have uploaded to the service, and see the file size, number of pages, and the upload date. The other cour columns "Imagemagick create page images", "Tesseract OCR", "Tesseract database", and "Processing status" all refer to the OCR-processing of pdfs, and is not relevant for those pdfs that contain digitized text.

On the second table, the user can start processing the uploaded pdfs, and also download a previously uploaded pdf, and delete an uploaded pdf. See Processing a file for more on processing files.

## Search

In this view you can search the Traitdata-database table for trait data saved from tables. As of now, you can only search by the scientific name of the species.

## Logout

You can log out of the service from here, press the new Logout -button to actually log out.
