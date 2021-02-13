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

# Metadata getters
def get_author(path_to_file: Path):
    doc = fitz.open(path_to_file)
    author = doc.metadata["author"]
    return author

def get_title(path_to_file: Path):
    doc = fitz.open(path_to_file)
    title = doc.metadata["title"]
    return title

# Main for testing
if __name__ == "__main__":
    data_directory = Path("../test_data/Books")

    files = []

    for file in os.listdir(data_directory):
        if path_to_file_has_file(data_directory / file):
            path_to_file = data_directory / file
            files.append(path_to_file)

    for file in files:
        print(f"Filename: {file.name}, author: {get_author(file)}, title: {get_title(file)}")