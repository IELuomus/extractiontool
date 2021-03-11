# Tests if pdf has any boxes that contain digitized text, and gives a ratio of the boxes that contain text / the total pdf surface area
# Usage: call pdf_sorter / is_text_pdf(path_to_data_directory_as_string, file_name_to_be_sorted_as_string) if it return True, it's most likely a text pdf, 
# and if it returns False, it's most likely an image-only pdf

import fitz
from pathlib import Path
import os

def get_text_percentage(file_name: str) -> float:
    """
    Calculate the percentage of document that is covered by (searchable) text.

    If the returned percentage of text is very low, the document is
    most likely a scanned PDF
    """
    total_page_area = 0.0
    total_text_area = 0.0

    doc = fitz.open(file_name)

    for page_num, page in enumerate(doc):
        total_page_area = total_page_area + abs(page.rect)
        text_area = 0.0
        for b in page.getTextBlocks(): # 0 to 3rd positions are the coordinates of the box, 4th contains the text or image info
            if b[6] == 0: # 6th position on the list is 0 if text, 1 if image
                r = fitz.Rect(b[:4])  # rectangle where block text appears
                text_area = text_area + abs(r)
        total_text_area = total_text_area + text_area
    doc.close()
    return total_text_area / total_page_area

# convert data directory and file name to Path-object
def path_to_file(data_directory: str, file_name: str):
    path = Path(data_directory)
    return path / file_name

# test if the given path contains a file
def path_to_file_has_file(path_to_file: Path):
    return os.path.isfile(path_to_file)

# Check if pdf contains digitized text or just images use threshold_for_text_pdf to determine the % of pdf area
# that needs to contain text containing boxes to determine. 
# Returns True if suffiziently texty, otherwise False
def is_text_pdf(data_directory: str, file_name: str):
    threshold_for_text_pdf = 0.05

    if path_to_file_has_file(path_to_file(data_directory, file)):
        text_perc = get_text_percentage(path_to_file(data_directory, file))

        if text_perc > threshold_for_text_pdf:
            return True
        else:
            return False

# main for testing, checks out all pdf's in the media/
if __name__ == "__main__": # analyzes a bunch of pdf's in a directory
    data_directory = "media/" # relative path to directory containing the pdf's to be analyzed

    files = os.listdir(data_directory)

    for file in files:

        text_perc = get_text_percentage(path_to_file(data_directory, file))

        if text_perc < 0.05:
            descriptor = "fully scanned PDF - no relevant text"
        else:
            descriptor = "not fully scanned PDF - text is present"

        print(f"{file:<50} - {text_perc:.2f} - {descriptor}")