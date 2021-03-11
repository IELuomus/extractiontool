import fitz
import io
import os
import csv
from pathlib import Path

# test if the given path contains a file
def path_to_file_has_file(path_to_file: Path):
    return os.path.isfile(path_to_file)

# read the text from the given pdf at the given path and output a txt-file
def pdf_to_txt(pdf_name: str, path_to_file: Path):
    if path_to_file_has_file(path_to_file): 
        doc = fitz.open(path_to_file)
        out = open("media/" + pdf_name + ".txt", "wb")
        for page in doc:
            text = page.getText().encode("utf8")
            out.write(text)
            out.write(bytes((12,)))
        out.close()

# read the text from the given pdf at the given path and output an xml
def pdf_to_xml(pdf_name: str, path_to_file: Path):
    if path_to_file_has_file(path_to_file): 
        doc = fitz.open(path_to_file)
        out = open(pdf_name + ".xml", "wb")
        for page in doc:
            text = page.getText("xml").encode("utf8")
            out.write(text)
            out.write(bytes((12,)))
        out.close()

# convert string-like list to list
def stringList_to_list(stringList: str):
    string = stringList.replace(')','').replace('(','')
    output = string.replace("'",'').split(",")
    return output

def str_is_int(test: str):
    try:
        int(test)
        return True
    except ValueError:
        return False

def str_is_float(test: str):
    try:
        float(test)
        return True
    except ValueError:
        return False

# Read text from a given pdf and outputs a list of pages containing a list with each word
# on that page with the coordinates of the box that contains the word, the word itself, and 
# additional information of the location of the word on the page, and the page number
# STRIPS SOME OF THE PUNCTUATION!
def pdf_to_words(pdf_name: str, path_to_file: Path):
    if path_to_file_has_file(path_to_file):
        doc = fitz.open(path_to_file)
        pages = []
        pagecounter = 1

        for page in doc:
            page_word_list = []
            words_on_page = page.getText("words")

            for word in words_on_page:
                word_to_list = stringList_to_list(str(word))
                word_to_list.append(pagecounter)

                # convert entries 0 to 3 into float, and 5 to 7 into int
                for i in range(len(word_to_list)):
                    if i >= 0 and i <= 3:
                        if str_is_float(word_to_list[i]):
                            converted_to_float = float(word_to_list[i])
                            word_to_list[i] = converted_to_float
                        else:
                            word_to_list[i] = None

                    if i >= 5 and i <= 7:
                        if str_is_int(word_to_list[i]):
                            converted_to_int = int(word_to_list[i])
                            word_to_list[i] = converted_to_int
                        else:
                            word_to_list[i] = None

                page_word_list.append(word_to_list)
            
            pages.append(page_word_list)
            pagecounter += 1

        return pages

# Metadata getters
def get_author(path_to_file: Path):
    if path_to_file_has_file(path_to_file):
        doc = fitz.open(path_to_file)
        author = doc.metadata["author"]
        return author

def get_title(path_to_file: Path):
    if path_to_file_has_file(path_to_file):
        doc = fitz.open(path_to_file)
        title = doc.metadata["title"]
        return title

def get_metadata(path_to_file: Path):
    if path_to_file_has_file(path_to_file):
        doc = fitz.open(path_to_file)
        metadata = doc.metadata
        return metadata
        
def path_to_file(data_directory: str, file_name: str):
    path = Path(data_directory)
    return path / file_name

# Main for testing
if __name__ == "__main__":
    data_directory = "media/"
    
    file_name = "mammalshb1.pdf"
    
    pages = pdf_to_words(path_to_file(data_directory, file_name))

    for page in pages:
        for word in page:
            print(f"{word}")

    
    # files = []

    # for file in os.listdir(data_directory):
    #     path_to_file = data_directory / file
        
    #     if path_to_file_has_file(path_to_file):
    #         files.append(path_to_file)

    # out = open("../test_data/results/" + source_directory + ".csv", "wb")
    # text = f"Filename; author; title; keywords; subject\n".encode("utf8")
    # out.write(text)
    # for file in files:
    #     metadata = get_metadata(file)
    #     text = f'{file.name}; {metadata["author"]}; {metadata["title"]}; {metadata["keywords"]}; {metadata["subject"]}\n'.encode("utf8")
    #     out.write(text)
    # out.close()