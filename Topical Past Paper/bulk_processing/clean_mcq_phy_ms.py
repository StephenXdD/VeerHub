import os
import fitz  # PyMuPDF
import re

# Mapping for months based on the paper letter
month_mapping = {
    's': 'May/June',
    'm': 'February/March',
    'w': 'October/November'
}

# Mapping for year
year_mapping = {
    '17': '2017',  # Example: '17' maps to '2017'
    '18': '2018',  # Example: '18' maps to '2018'
    '19': '2019',  # Example: '19' maps to '2019'
    '20': '2020',  # Example: '20' maps to '2020'
    '21': '2021',  # Example: '21' maps to '2021'
    '22': '2022',  # Example: '22' maps to '2022'
    # Add more mappings as needed
}

def get_dynamic_texts_to_remove(file_name):
    # Base texts to remove
    base_texts_to_remove = [
        "Answer all the questions in the spaces provided.",
        "PUBLISHED",
        "Cambridge International AS & A Level – Mark Scheme",
        "March 2021",
        "March 2020",
        "March 2019",
        "March 2018",
        "March 2017",
        "Cambridge International AS/A Level – Mark Scheme",
        "Page 2 of 3",
        "Page 3 of 3",
        "February/March ",
        "2024",
        "© Cambridge University Press & Assessment 2024",
        "2023",
        "© UCLES ",
        "May/June ",
        "May/June",
        "icpa",
        "October/Nove"
    ]
    
    # Extract the year suffix, paper code, and letter (m, s, w) from the filename
    match = re.match(r"(\d+)_([smw])(\d+)_ms_(\d+)\.pdf", file_name)
    if match:
        paper_code = match.group(1)
        paper_letter = match.group(2)
        year_suffix = match.group(3)  # This will be used to map to the year
        paper_number = match.group(4)

        # Construct the subject code/paper number text (e.g., "9702/11")
        subject_code_paper_number = f"{paper_code}/{paper_number}"
        base_texts_to_remove.append(subject_code_paper_number)

        # Construct the dynamic mapping text (e.g., "May/June 2022")
        mapped_month_year = f"{month_mapping.get(paper_letter, '')} {year_mapping.get(year_suffix, '2022')}"
        base_texts_to_remove.append(mapped_month_year)

        # Construct the dynamic copyright year (e.g., "© UCLES 2017")
        copyright_year_text = f"© UCLES {year_mapping.get(year_suffix, '2017')}"
        base_texts_to_remove.append(copyright_year_text)

    return base_texts_to_remove

def remove_specific_text(input_path, output_path, texts_to_remove=None):
    # Open the input PDF
    pdf_document = fitz.open(input_path)
    
    # Create a new PDF to store the processed content
    output_pdf = fitz.open()

    # If no specific texts are provided, use an empty list
    if texts_to_remove is None:
        texts_to_remove = []
    
    # Iterate over all pages except the first one
    for page_num in range(1, pdf_document.page_count):
        page = pdf_document.load_page(page_num)  # Load page
        
        # Redact specific texts
        for text in texts_to_remove:
            # Search for all instances of the text and redact them
            text_instances = page.search_for(text)
            for instance in text_instances:
                page.add_redact_annot(instance)  # Redact the found text

        # Apply the redactions (removes the redacted content)
        page.apply_redactions()

        # Add the processed page to the output PDF
        output_pdf.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
    
    # Save the output PDF
    output_pdf.save(output_path)

def process_pdfs_in_folder(input_folder, output_folder):
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # List all files in the folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, "cleaned_" + filename)

            # Get the dynamic texts to remove based on the filename
            texts_to_remove = get_dynamic_texts_to_remove(filename)

            # Remove specific text, then save to the output folder
            remove_specific_text(input_path, output_path, texts_to_remove=texts_to_remove)
            print(f"Processed {filename}, saved to {output_path}")

if __name__ == "__main__":
    # Specify the folder where your PDFs are located
    input_folder = "input_pdfs"
    
    # Specify the output folder where cleaned PDFs will be saved (outside the input folder)
    output_folder = os.path.join(os.path.dirname(input_folder), 'output_cleaned')
    
    # Process all PDFs in the folder
    process_pdfs_in_folder(input_folder, output_folder)
