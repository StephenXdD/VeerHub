import os
import fitz  # PyMuPDF

def remove_text_from_pdf(input_pdf, output_pdf, text_to_remove, top_specific_texts, top_region_height=40):
    doc = fitz.open(input_pdf)
    
    # Loop through each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)

        # General text removal (from the entire page)
        for text in text_to_remove:
            areas = page.search_for(text)
            for area in areas:
                page.add_redact_annot(area)

        # Specific text removal (within the top 40-point region)
        top_region_rect = fitz.Rect(0, 0, page.rect.width, top_region_height)  # Define the top region
        for text in top_specific_texts:
            areas = page.search_for(text, clip=top_region_rect)  # Limit search to the top region
            for area in areas:
                page.add_redact_annot(area)

        # Apply all redactions for the current page
        page.apply_redactions()

    # Save the modified PDF
    doc.save(output_pdf)
    doc.close()

    print(f"Cleaned PDF saved as {output_pdf}")

def process_pdfs_in_directory(input_folder, output_folder, text_to_remove, top_specific_texts, top_region_height=40):
    # Walk through all subdirectories and files in the input folder
    for root, _, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(".pdf"):
                input_path = os.path.join(root, file_name)

                # Construct the path for the cleaned version, maintaining subdirectory structure
                relative_path = os.path.relpath(root, input_folder)
                output_path_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_path_dir, exist_ok=True)
                output_path = os.path.join(output_path_dir, file_name)

                # Remove the specified text from the PDF and save the cleaned version
                remove_text_from_pdf(input_path, output_path, text_to_remove, top_specific_texts, top_region_height=top_region_height)

# Folder paths
input_folder = "output_cleaned"  # Folder containing the PDFs to clean (with subdirectories)
output_folder = "cleaned_pdfs"  # Folder to save the cleaned PDFs, maintaining the same directory structure

# General list of text patterns to remove
text_to_remove = [
"Cambridge International AS/A Level – Mark Scheme", "PUBLISHED", '9709/12', "© UCLES 2018", "© UCLES 2019", "© UCLES 2020", "© UCLES 2021", "© UCLES 2022", "© UCLES 2023", "© UCLES 2024", "© UCLES 2017", "© UCLES 2016", "© UCLES 2015", "© UCLES 2014", "© UCLES 2013", "© UCLES 2012", "© UCLES 2011", "© UCLES 2010", "© UCLES 2009", "© UCLES 2008", "© UCLES 2007", "© UCLES 2006", "© UCLES 2005", "© UCLES 2003", "© UCLES 2002", "© UCLES 2004", "9709/13", "9709/11", "Page 1 of 7", "Page 2 of 7", "Page 3 of 7", "Page 4 of 7", "Page 5 of 7", "Page 6 of 7", "Page 7 of 7", "Page 1 of 8", "Page 2 of 8", "Page 3 of 8", "Page 4 of 8", "Page 5 of 8", "Page 6 of 8", "Page 7 of 8", "Page 8 of 8", "Page 1 of 9", "Page 2 of 9", "Page 3 of 9", "Page 4 of 9", "Page 5 of 9", "Page 6 of 9", "Page 7 of 9", "Page 8 of 9", "Page 9 of 9", "Page 1 of 10", "Page 2 of 10", "Page 3 of 10", "Page 4 of 10", "Page 5 of 10", "Page 6 of 10", "Page 7 of 10", "Page 8 of 10", "Page 9 of 10", "Page 10 of 10", "Page 1 of 11", "Page 2 of 11", "Page 3 of 11", "Page 4 of 11", "Page 5 of 11", "Page 6 of 11", "Page 7 of 11", "Page 8 of 11", "Page 9 of 11", "Page 10 of 11", "Page 11 of 11", "Page 1 of 12", "Page 2 of 12", "Page 3 of 12", "Page 4 of 12", "Page 5 of 12", "Page 6 of 12", "Page 7 of 12", "Page 8 of 12", "Page 9 of 12", "Page 10 of 12", "Page 11 of 12", "Page 12 of 12", "Page 1 of 13", "Page 2 of 13", "Page 3 of 13", "Page 4 of 13", "Page 5 of 13", "Page 6 of 13", "Page 7 of 13", "Page 8 of 13", "Page 9 of 13", "Page 10 of 13", "Page 11 of 13", "Page 12 of 13", "Page 13 of 13", "Page 1 of 14", "Page 2 of 14", "Page 3 of 14", "Page 4 of 14", "Page 5 of 14", "Page 6 of 14", "Page 7 of 14", "Page 8 of 14", "Page 9 of 14", "Page 10 of 14", "Page 11 of 14", "Page 12 of 14", "Page 13 of 14", "Page 14 of 14", "Page 1 of 15", "Page 2 of 15", "Page 3 of 15", "Page 4 of 15", "Page 5 of 15", "Page 6 of 15", "Page 7 of 15", "Page 8 of 15", "Page 9 of 15", "Page 10 of 15", "Page 11 of 15", "Page 12 of 15", "Page 13 of 15", "Page 14 of 15", "Page 15 of 15", "Cambridge International AS & A Level – Mark Scheme", "Page 1 of 16", "Page 2 of 16", "Page 3 of 16", "Page 4 of 16", "Page 5 of 16", "Page 6 of 16", "Page 7 of 16", "Page 8 of 16", "Page 9 of 16", "Page 10 of 16", "Page 11 of 16", "Page 12 of 16", "Page 13 of 16", "Page 14 of 16", "Page 15 of 16", "Page 16 of 16", "Page 1 of 17", "Page 2 of 17", "Page 3 of 17", "Page 4 of 17", "Page 5 of 17", "Page 6 of 17", "Page 7 of 17", "Page 8 of 17", "Page 9 of 17", "Page 10 of 17", "Page 11 of 17", "Page 12 of 17", "Page 13 of 17", "Page 14 of 17", "Page 15 of 17", "Page 16 of 17", "Page 17 of 17", "Page 1 of 19", "Page 2 of 19", "Page 3 of 19", "Page 4 of 19", "Page 5 of 19", "Page 6 of 19", "Page 7 of 19", "Page 8 of 19", "Page 9 of 19", "Page 10 of 19", "Page 11 of 19", "Page 12 of 19", "Page 13 of 19", "Page 14 of 19", "Page 15 of 19", "Page 16 of 19", "Page 17 of 19", "Page 18 of 19", "Page 19 of 19"
"Page 1 of 18", "Page 2 of 18", "Page 3 of 18", "Page 4 of 18", "Page 5 of 18", "Page 6 of 18", "Page 7 of 18", "Page 8 of 18", "Page 9 of 18", "Page 10 of 18", "Page 11 of 18", "Page 12 of 18", "Page 13 of 18", "Page 14 of 18", "Page 15 of 18", "Page 16 of 18", "Page 17 of 18", "Page 18 of 18","Page 1 of 20", "Page 2 of 20", "Page 3 of 20", "Page 4 of 20", "Page 5 of 20", "Page 6 of 20", "Page 7 of 20", "Page 8 of 20", "Page 9 of 20", "Page 10 of 20", "Page 11 of 20", "Page 12 of 20", "Page 13 of 20", "Page 14 of 20", "Page 15 of 20", "Page 16 of 20", "Page 17 of 20", "Page 18 of 20", "Page 19 of 20", "Page 20 of 20", "Page 1 of 21", "Page 2 of 21", "Page 3 of 21", "Page 4 of 21", "Page 5 of 21", "Page 6 of 21", "Page 7 of 21", "Page 8 of 21", "Page 9 of 21", "Page 10 of 21", "Page 11 of 21", "Page 12 of 21", "Page 13 of 21", "Page 14 of 21", "Page 15 of 21", "Page 16 of 21", "Page 17 of 21", "Page 18 of 21", "Page 19 of 21", "Page 20 of 21", "Page 21 of 21", "Page 1 of 22", "Page 2 of 22", "Page 3 of 22", "Page 4 of 22", "Page 5 of 22", "Page 6 of 22", "Page 7 of 22", "Page 8 of 22", "Page 9 of 22", "Page 10 of 22", "Page 11 of 22", "Page 12 of 22", "Page 13 of 22", "Page 14 of 22", "Page 15 of 22", "Page 16 of 22", "Page 17 of 22", "Page 18 of 22", "Page 19 of 22", "Page 20 of 22", "Page 21 of 22", "Page 22 of 22", "Page 1 of 23", "Page 2 of 23", "Page 3 of 23", "Page 4 of 23", "Page 5 of 23", "Page 6 of 23", "Page 7 of 23", "Page 8 of 23", "Page 9 of 23", "Page 10 of 23", "Page 11 of 23", "Page 12 of 23", "Page 13 of 23", "Page 14 of 23", "Page 15 of 23", "Page 16 of 23", "Page 17 of 23", "Page 18 of 23", "Page 19 of 23", "Page 20 of 23", "Page 21 of 23", "Page 22 of 23", "Page 23 of 23", "© Cambridge International Examinations 2010", "© Cambridge International Examinations 2011", "© Cambridge International Examinations 2012", "© Cambridge International Examinations 2013", "© Cambridge International Examinations 2014", "© Cambridge International Examinations 2015", "© Cambridge International Examinations 2016", 'Page 4', 'Page 5', 'Page 6', 'Page 7', 'Page 8', 'Page 9', "Mark Scheme", "Syllabus", "Paper", "9709"
# Extend as needed
]

# Specific texts to remove within the top 40-point region
top_specific_texts = ["0", "1", "2", "3", "4", "5", "6", "7","8", "9", "10", "11", "12"]

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each PDF in the directory and its subdirectories
process_pdfs_in_directory(input_folder, output_folder, text_to_remove, top_specific_texts, top_region_height=40)
