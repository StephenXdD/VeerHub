import os
from PyPDF2 import PdfReader, PdfWriter

def rotate_pdf(input_pdf, output_pdf):
    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    # Rotate each page by 90 degrees
    for page in reader.pages:
        page.rotate(90)  # Rotate each page by 90 degrees clockwise
        writer.add_page(page)

    # Write the rotated PDF to the output file
    with open(output_pdf, "wb") as out_file:
        writer.write(out_file)

    print(f"Rotated file saved as {output_pdf}")

def process_pdfs_in_directory(input_folder, output_folder):
    # Walk through all subdirectories and files in the input folder
    for root, _, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith(".pdf"):
                input_path = os.path.join(root, file_name)

                # Construct the path for the rotated version, maintaining subdirectory structure
                relative_path = os.path.relpath(root, input_folder)
                output_path_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_path_dir, exist_ok=True)
                output_path = os.path.join(output_path_dir, file_name)

                # Rotate the PDF and save to the new location
                rotate_pdf(input_path, output_path)

# Folder paths
input_folder = "cropped_questions"  # Folder containing the original PDFs (with subdirectories)
output_folder = "final"  # Folder to save the rotated PDFs, maintaining the same directory structure

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Process each PDF in the directory and its subdirectories
process_pdfs_in_directory(input_folder, output_folder)