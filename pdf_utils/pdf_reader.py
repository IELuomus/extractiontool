import fitz
import io
import os
from pathlib import Path

# test if the given path contains a file
def path_to_file_has_file(path_to_file: Path):
    return os.path.isfile(path_to_file)

# read the text from the given pdf at the given path and output a txt
def pdf_to_txt(pdf_name: str, path_to_file: Path):
    doc = fitz.open(path_to_file)
    out = open(pdf_name + ".txt", "wb")
    for page in doc:
        text = page.getText().encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()

# read the text from the given pdf at the given path and output as 
def pdf_to_xml(pdf_name: str, path_to_file: Path):
    doc = fitz.open(path_to_file)
    out = open(pdf_name + ".xml", "wb")
    for page in doc:
        text = page.getText("xml").encode("utf8")
        out.write(text)
        out.write(bytes((12,)))
    out.close()
    
# Metadata getters
def get_author(path_to_file: Path):
    doc = fitz.open(path_to_file)
    author = doc.metadata["author"]
    return author

def get_title(path_to_file: Path):
    doc = fitz.open(path_to_file)
    title = doc.metadata["title"]
    return title

def get_metadata(path_to_file: Path):
    doc = fitz.open(path_to_file)
    metadata = doc.metadata
    return metadata

# Main for testing
if __name__ == "__main__":
    test_data_path = "../test_data/"
    source_directory = "Other"
    source = test_data_path + source_directory
    data_directory = Path(source)

    file_name = "mammalshb1.pdf"
    
    path_to_file = data_directory / file_name

    pdf_to_xml(file_name, path_to_file)
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