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
    ]
    
    match = re.match(r"(\d+)_([smw])(\d+)_qp_(\d+)", file_name)
    if match:
        paper_code = match.group(1)
        letter = match.group(2)
        year_suffix = match.group(3)
        paper_number = match.group(4)

        paper_number = paper_number.zfill(2)
        year_suffix = year_suffix.zfill(2)

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

def remove_headers_footers_and_specific_pages(input_pdf, output_pdf, texts_to_remove, blank_page_text="BLANK PAGE", header_height=50, page_number_height=50):
    pdf_document = fitz.open(input_pdf)
    
    # Remove the first two pages
    if len(pdf_document) > 1:
        pdf_document.delete_page(0)  # Remove the first page
        pdf_document.delete_page(0)  # Remove the second page (Note: After removing the first, the next page becomes index 0)

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

        if "FORMULAE" in page_text and "UNIFORMLY ACCELERATED MOTION" in page_text:
            pages_to_delete.append(page_number)
        
        if "DATA" in page_text and "SPEED OF LIGHT IN FREE SPACE" in page_text:
            pages_to_delete.append(page_number)

        # Define the top region where headers and page numbers may be located
        header_area = fitz.Rect(0, 0, page_width, header_height)
        center_x = page_width / 2

        # Redact potential page numbers and text in the header area
        for block in page.get_text("blocks"):
            x0, y0, x1, y1, text = block[:5]
            if header_area.intersects(fitz.Rect(x0, y0, x1, y1)):
                if text.strip().isdigit() or re.match(r"^\d+[-/]*$", text.strip()):
                    # Redact numeric text (page numbers)
                    page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))

        # Specifically handle centered page numbers
        centered_number_area = fitz.Rect(center_x - 50, 0, center_x + 50, page_number_height)
        for block in page.get_text("blocks"):
            x0, y0, x1, y1, text = block[:5]
            if centered_number_area.intersects(fitz.Rect(x0, y0, x1, y1)) and text.strip().isdigit():
                # Redact text if it looks like a centered page number
                page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))

        # Redact other texts in texts_to_remove
        for text in texts_to_remove:
            for rect in page.search_for(text, quads=True):
                page.add_redact_annot(rect)

        page.apply_redactions()

    # Delete unwanted pages in reverse order
    for page_number in reversed(pages_to_delete):
        pdf_document.delete_page(page_number)

    # Handle the last page to remove everything below 150 points from the bottom of the page
    if len(pdf_document) > 0:
        last_page = pdf_document[-1]

        rects = last_page.get_text("blocks")
        for block in rects:
            if len(block) >= 5:
                x0, y0, x1, y1, _, text, _ = block
                if (y0 > last_page.rect.height - 60) and (y1 - y0 < 5):
                    last_page.add_redact_annot(fitz.Rect(x0, y0, x1, y1))

        bottom_y = last_page.rect.height
        cutoff_y = bottom_y - 160
        last_page.add_redact_annot(fitz.Rect(0, cutoff_y, last_page.rect.width, bottom_y))
        last_page.apply_redactions()

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
