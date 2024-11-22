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
        "[Total: 30]",  # Add the text to remove
        "[Total: 15]",
        "06_9706_12_2024_1.13b",
        "Answer all the questions in the spaces provided.",
        "Space for working"
    ]
    
    # Extract parts of the file name to construct dynamic text
    match = re.match(r"(\d+)_([smw])(\d+)_qp_(\d+)", file_name)
    if match:
        paper_code = match.group(1)
        letter = match.group(2)
        year_suffix = match.group(3)
        paper_number = match.group(4)

        # Construct copyright year
        copyright_year = f"© UCLES 20{year_suffix}"
        dynamic_text = f"{paper_code}/{paper_number}/{mapping.get(letter, '')}/{year_suffix}"

        return base_texts_to_remove + [copyright_year, dynamic_text]
    
    return base_texts_to_remove

def remove_headers_footers_and_specific_pages(input_pdf, output_pdf, texts_to_remove, blank_page_text="BLANK PAGE", header_height=50):
    pdf_document = fitz.open(input_pdf)
    
    # Remove the first two pages explicitly
    if len(pdf_document) > 1:
        pdf_document.delete_page(0)  # Remove the first page
        pdf_document.delete_page(0)  # Remove the second page (originally the third page)

    pages_to_delete = []

    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        page_width = page.rect.width

        # Redact the header content by targeting the top of the page (header area)
        header_text_instances = page.get_text("blocks")
        for block in header_text_instances:
            x0, y0, x1, y1, _, text, _ = block
            if y0 <= header_height:  # If the text block is within the header area
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))  # Redact the header content

        # Check for "Formulae" only in the first 3 pages
        page_text = page.get_text("text").upper()  # Case insensitive search
        if page_number < 3 and "FORMULAE" in page_text:  # Only check for "Formulae" in the first 3 pages
            pages_to_delete.append(page_number)

        # Mark pages for deletion based on specific text conditions
        if blank_page_text in page_text or "BEGINS ON PAGE" in page_text or "ADDITIONAL PAGE" in page_text:
            pages_to_delete.append(page_number)
        if "IS ON THE NEXT PAGE." in page_text:
            pages_to_delete.append(page_number)
        if "PLEASE TURN OVER" in page_text:
            pages_to_delete.append(page_number)

    # Delete unwanted pages in reverse order
    for page_number in reversed(pages_to_delete):
        pdf_document.delete_page(page_number)

    # Redact specific texts in remaining pages
    for page_number in range(len(pdf_document)):
        page = pdf_document[page_number]
        
        # Redact case-sensitive words "For", "Examiner's", and "Use"
        case_sensitive_words = ["For", "Examiner’s", "Use","Examiner’s ", " Examiner’s"]
        for word in case_sensitive_words:
            for instance in page.search_for(word):
                matched_text = page.get_text("text", clip=instance)
                if matched_text.strip() == word:
                    page.add_redact_annot(instance)

        # Redact other texts in texts_to_remove, case-insensitive
        for text in texts_to_remove:
            for rect in page.search_for(text):
                page.add_redact_annot(rect)
        page.apply_redactions()  # Apply all redactions for this page

        # Remove page numbers in the header area
        header_text_instances = page.get_text("blocks")
        for block in header_text_instances:
            x0, y0, x1, y1, _, text, _ = block
            if y0 <= header_height and abs(x0 + (x1 - x0) / 2 - page_width / 2) < 20:  # Centered header
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))  # Redact header content
        page.apply_redactions()  # Apply redactions to remove page numbers

    # Handle the last page to remove everything below 30 points from the bottom of the page
    if len(pdf_document) > 0:
        last_page = pdf_document[-1]

        # Remove any horizontal line above the footer text
        rects = last_page.get_text("blocks")
        for block in rects:
            if len(block) >= 5:
                x0, y0, x1, y1, _, text, _ = block
                if (y0 > last_page.rect.height - 60) and (y1 - y0 < 5):  # Height threshold for a line
                    last_page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))

        # Reduce the footer removal by adjusting the cutoff_y
        bottom_y = last_page.rect.height
        cutoff_y = bottom_y - 100  # Adjust this value to reduce the amount of footer removed
        last_page.add_redact_annot(fitz.Rect(0, cutoff_y, last_page.rect.width, bottom_y))  # Redact everything below cutoff_y

        last_page.apply_redactions()  # Apply all redactions for the last page

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
