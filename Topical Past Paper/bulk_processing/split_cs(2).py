import os
import fitz  # PyMuPDF
import re
import shutil

# Define the regex pattern to detect only subparts like (a), (b), etc.
subpart_pattern = re.compile(r'\((a|b|c|d|e|f|g|h|i|j)\)')  # Matches subparts like (a), (b), (c), ...

# Function to check subparts within a specific region of a PDF file
def process_subparts_in_pdf(input_pdf, output_dir):
    # Open the PDF document
    pdf_document = fitz.open(input_pdf)

    # Extract the base filename (e.g., "1 (a) 1 (b).pdf")
    base_name = os.path.basename(input_pdf)
    
    # Create the output folder if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Flag to check if any subparts are found
    subparts_found = False

    # Variable to track the current subpart and accumulate pages for it
    current_subpart = None
    current_pdf_document = None
    
    # Iterate through each page and check for subparts within the defined region (x=70 to x=87)
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Define the region to search (x=70 to x=87 from the left, full height of the page)
        region = fitz.Rect(70, 0, 87, page.rect.height)
        
        # Extract text from the defined region only
        page_text = page.get_text("text", clip=region)
        
        # Search for subparts on the page
        subparts = subpart_pattern.findall(page_text)

        if subparts:
            # If a new subpart is found, save the previous subpart PDF if any
            if current_subpart:
                # Save the current subpart PDF before starting a new one
                output_pdf_path = os.path.join(output_dir, f"{base_name.strip('.pdf')} ({current_subpart}).pdf")
                current_pdf_document.save(output_pdf_path)
                print(f"Saved subpart PDF: {output_pdf_path}")
                current_pdf_document.close()
            
            # Start a new subpart and create a new PDF document for it
            current_subpart = subparts[0]  # Take the first subpart found (e.g., (a))
            current_pdf_document = fitz.open()
            current_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)
            subparts_found = True
        else:
            # If no subpart is found, continue adding pages to the current subpart PDF
            if current_subpart:
                current_pdf_document.insert_pdf(pdf_document, from_page=page_num, to_page=page_num)

    # If any subpart was found, save the last subpart PDF
    if current_subpart and current_pdf_document:
        output_pdf_path = os.path.join(output_dir, f"{base_name.strip('.pdf')} ({current_subpart}).pdf")
        current_pdf_document.save(output_pdf_path)
        print(f"Saved subpart PDF: {output_pdf_path}")
        current_pdf_document.close()

    # If no subparts are found, copy the original file to the output directory without changes
    if not subparts_found:
        output_pdf_path = os.path.join(output_dir, base_name)
        shutil.copy(input_pdf, output_pdf_path)
        print(f"No subparts found. Copied original file to: {output_pdf_path}")


# Function to recursively traverse the directory and process subparts
def process_subparts_in_directory(input_directory, output_directory):
    # Traverse through all subfolders in the output_questions directory
    for root, dirs, files in os.walk(input_directory):
        for file in files:
            if file.endswith(".pdf"):
                input_pdf = os.path.join(root, file)
                
                # Generate corresponding output directory in the "temp" folder
                relative_path = os.path.relpath(root, input_directory)
                output_dir = os.path.join(output_directory, relative_path)
                
                # Process the subparts in the current PDF
                process_subparts_in_pdf(input_pdf, output_dir)


# Main function to initiate the process
def main():
    input_directory = "output_questions"  # Folder containing the question PDFs
    output_directory = "temp"  # Folder where subpart PDFs will be saved

    # Ensure the "temp" directory is clean before starting
    if os.path.exists(output_directory):
        shutil.rmtree(output_directory)
    os.makedirs(output_directory)

    # Process the subparts in all PDFs in the input directory
    process_subparts_in_directory(input_directory, output_directory)


# Run the script
if __name__ == "__main__":
    main()
