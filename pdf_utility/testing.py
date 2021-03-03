import fitz
import io
import os
import csv
from pathlib import Path

from .pdf_reader import pdf_to_words

# Main for testing
if __name__ == "__main__":
    test_data_path = "../test_data/"
    source_directory = "Other"
    source = test_data_path + source_directory
    data_directory = Path(source)

    file_name = "mammalshb1.pdf"
    
    path_to_file = data_directory / file_name

    pages = pdf_to_words(file_name, path_to_file)

    for page in pages:
        for word in page:
            print(f"{word}")

    
    # files = []

    # for file in os.listdir(data_directory):
    #     path_to_file = data_directory / file
        
    #     if pdf_reader.path_to_file_has_file(path_to_file):
    #         files.append(path_to_file)

    # out = open("../test_data/results/" + source_directory + ".csv", "wb")
    # text = f"Filename; author; title; keywords; subject\n".encode("utf8")
    # out.write(text)
    # for file in files:
    #     metadata = get_metadata(file)
    #     text = f'{file.name}; {metadata["author"]}; {metadata["title"]}; {metadata["keywords"]}; {metadata["subject"]}\n'.encode("utf8")
    #     out.write(text)
    # out.close()