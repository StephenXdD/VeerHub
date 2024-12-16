import os
import fitz  # PyMuPDF
from PIL import Image

# Set paths
input_folder = os.path.expanduser("~/Desktop/output_questions")
output_folder = os.path.expanduser("~/Desktop/temp")

# Walk through all subdirectories in the input folder
for root, dirs, files in os.walk(input_folder):
    for file in files:
        # Check if the file is a PDF
        if file.endswith('.pdf'):
            # Build full input and output paths
            input_path = os.path.join(root, file)
            
            # Create corresponding subdirectory structure in the output folder
            relative_path = os.path.relpath(root, input_folder)
            output_path = os.path.join(output_folder, relative_path, file.replace('.pdf', '.png'))
            output_dir = os.path.dirname(output_path)
            
            # Create directories if they don't exist
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # Open the PDF file
            pdf_document = fitz.open(input_path)
            
            # Convert the first page of the PDF to an image
            page = pdf_document.load_page(0)
            pix = page.get_pixmap()
            
            # Convert the pixmap to a Pillow image
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            
            # Save the image
            img.save(output_path, "PNG")
            
            print(f"Converted {input_path} to {output_path}")
