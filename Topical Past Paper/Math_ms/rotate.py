import os
from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf(input_pdf, output_pdf):
    """
    Rotates each page of the input PDF by 270 degrees and saves the result as a new file.
    """
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    for page in reader.pages:
        page.rotate(270)  # Rotate each page by 270 degrees clockwise
        writer.add_page(page)

    with open(output_pdf, "wb") as out_file:
        writer.write(out_file)

    print(f"Rotated file saved as {output_pdf}")

def process_pdfs_in_directory(input_folder, output_folder):
    """
    Processes all PDF files in a directory and its subdirectories.
    Saves the rotated files with the same relative path in the output directory.
    """
    for root, _, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(".pdf"):
                input_path = os.path.join(root, file_name)

                # Construct the exact same path structure within the output folder
                relative_path = os.path.relpath(input_path, input_folder)
                output_path = os.path.join(output_folder, relative_path)

                # Ensure the output directory exists
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                # Rotate the PDF and save to the same relative path in the output folder
                rotate_pdf(input_path, output_path)

# Folder paths
input_folder = "output_cleaned"  # Folder containing the original PDFs (with subdirectories)
output_folder = "rotated_pdfs"  # Root folder to save the rotated PDFs

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process PDFs
process_pdfs_in_directory(input_folder, output_folder)
