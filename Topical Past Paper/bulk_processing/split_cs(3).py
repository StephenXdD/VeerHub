import os
import fitz  # PyMuPDF
import re  # For regular expressions
import shutil  # For copying files

# Directory paths
input_directory = r"temp"
output_directory = r"temp_output"

# Ensure output directory exists
if not os.path.exists(output_directory):
    os.makedirs(output_directory)

# Regular expression to match second subparts like (i), (ii), (iii), etc.
second_subpart_pattern = r"\((i|ii|iii|iv|v|vi|vii|viii|ix|x)\)"

# Function to process PDFs in the input directory
def process_pdfs(input_dir):
    for subdir, dirs, files in os.walk(input_dir):
        for file in files:
            if file.endswith(".pdf"):
                file_path = os.path.join(subdir, file)
                print(f"Processing {file_path}...")

                # Process the file to extract the text between 70 and 108 units from the left
                process_pdf(file_path, subdir, file)

# Function to process individual PDF and find occurrences of (i), (ii), (iii), etc. in the specified region
def process_pdf(file_path, subdir, file_name):
    pdf_document = fitz.open(file_path)
    
    # List to store second subparts found (if any)
    second_subparts = []

    # Iterate through all pages of the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document[page_num]
        page_text_blocks = page.get_text("blocks")  # Get text blocks with positions

        for block in page_text_blocks:
            bbox, text = block[:4], block[4].strip()  # Extract bounding box and clean text

            # Check if the block is within the region before 50 points from the left (i.e., bbox[0] < 50)
            if bbox[0] < 50:  # bbox[0] is the left margin (x-coordinate)
                # Search for second subpart occurrences (i), (ii), (iii), etc.
                matches = re.findall(second_subpart_pattern, text)
                if matches:
                    second_subparts.extend(matches)
    
    # If second subparts are found, rename and save the PDF for each second subpart
    if second_subparts:
        for i, second_subpart in enumerate(second_subparts):
            # Generate new file name based on the second subpart
            base_name = file_name.split(".pdf")[0]  # Get the base name without extension
            new_file_name = f"{base_name} ({second_subpart}).pdf"
            
            # Construct full output path while maintaining the subdirectory structure
            output_subdir = os.path.join(output_directory, os.path.relpath(subdir, input_directory))
            if not os.path.exists(output_subdir):
                os.makedirs(output_subdir)  # Create the subdirectories if they don't exist

            new_output_path = os.path.join(output_subdir, new_file_name)
            print(f"Saving {new_file_name}...")

            # Copy the original PDF to the new output path
            shutil.copy(file_path, new_output_path)
    else:
        # If no second subparts are found, just copy the original file without renaming
        output_subdir = os.path.join(output_directory, os.path.relpath(subdir, input_directory))
        if not os.path.exists(output_subdir):
            os.makedirs(output_subdir)  # Create the subdirectories if they don't exist

        output_path = os.path.join(output_subdir, file_name)
        shutil.copy(file_path, output_path)
        print(f"Copied {file_name} without changes.")

# Run the script
process_pdfs(input_directory)
