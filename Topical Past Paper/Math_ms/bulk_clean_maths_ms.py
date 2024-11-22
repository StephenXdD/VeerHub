import fitz  # PyMuPDF
import os
import re

# Define the mapping for month abbreviations
mapping = {
    's': 'M/J',  # Mapping for 's'
    'm': 'F/M',  # Mapping for 'm'
    'w': 'O/N'   # Mapping for 'w'
}

def get_texts_to_remove(file_name):
    base_texts_to_remove = [
        "www.dynamicpapers.com", 
        "[Turn over", 
        "[Turn over ", 
        "DO NOT WRITE IN THIS MARGIN",
        "[Total: 30]", 
        "[Total: 15]",
        "06_9706_12_2024_1.13b",
        "Answer all the questions in the spaces provided."
    ]
    
    # Extract parts of the file name to construct dynamic text
    match = re.match(r"(\d+)_([smw])(\d+)_qp_(\d+)", file_name)
    if match:
        paper_code = match.group(1)
        letter = match.group(2)
        year_suffix = match.group(3)
        paper_number = match.group(4)

        # Ensure paper_number and year_suffix are two digits
        paper_number = paper_number.zfill(2)
        year_suffix = year_suffix.zfill(2)

        # Construct dynamic text formats
        dynamic_text_with_slash = f"{paper_code}/{paper_number}/{mapping.get(letter, '')}/{year_suffix}"
        dynamic_text_without_slash = f"{paper_code}_{paper_number}_{mapping.get(letter, '')}{year_suffix}"
        copyright_year = f"© UCLES 20{year_suffix}"
        dynamic_text_no_slash_final = f"{paper_code}/{paper_number}/{mapping.get(letter, '')}{year_suffix}"
        dynamic_text_generic = f"{paper_code}/{paper_number}/{mapping.get(letter, '')}/{year_suffix}"

        return base_texts_to_remove + [
            copyright_year, 
            dynamic_text_with_slash, 
            dynamic_text_without_slash,
            dynamic_text_no_slash_final, 
            dynamic_text_generic
        ]
    
    return base_texts_to_remove

def remove_headers_footers_and_specific_pages(input_pdf, output_pdf, texts_to_remove, blank_page_text="BLANK PAGE"):
    pdf_document = fitz.open(input_pdf)
    
    # Remove the first three pages
    for _ in range(min(3, len(pdf_document))):  # Ensure we don't try to remove more pages than exist
        pdf_document.delete_page(0)

    pages_to_delete = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        page_width = page.rect.width

        # Mark pages for deletion based on specific text conditions
        page_text = page.get_text("text").upper()
        if blank_page_text in page_text or "ADDITIONAL PAGE" in page_text:
            pages_to_delete.append(page_number)
        elif "PLEASE TURN OVER" in page_text:
            pages_to_delete.append(page_number)

        # Check if page contains both "Formulae" and "uniformly accelerated motion"
        if "FORMULAE" in page_text and "UNIFORMLY ACCELERATED MOTION" in page_text:
            pages_to_delete.append(page_number)
        
        # Check if page contains both "Data" and "speed of light in free space"
        if "DATA" in page_text and "SPEED OF LIGHT IN FREE SPACE" in page_text:
            pages_to_delete.append(page_number)

        # Redact any text found in the 'texts_to_remove' list (case-insensitive)
        for text in texts_to_remove:
            for rect in page.search_for(text, quads=True):
                page.add_redact_annot(rect)
        
        page.apply_redactions()  # Apply all redactions for this page

    # Delete unwanted pages in reverse order
    for page_number in reversed(pages_to_delete):
        pdf_document.delete_page(page_number)

    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    pdf_document.save(output_pdf)
    pdf_document.close()

# Bulk processing
input_directory = "input_pdfs"
output_directory = "output_cleaned"

for file_name in os.listdir(input_directory):
    if file_name.endswith(".pdf"):
        input_pdf_path = os.path.join(input_directory, file_name)
        output_pdf_path = os.path.join(output_directory, f"{file_name.replace('.pdf', '_cleaned.pdf')}")

        texts_to_remove = get_texts_to_remove(file_name)
        remove_headers_footers_and_specific_pages(input_pdf_path, output_pdf_path, texts_to_remove)

print("Bulk cleaning completed.")
