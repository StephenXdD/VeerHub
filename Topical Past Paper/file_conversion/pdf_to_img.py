import os
from pdf2image import convert_from_path

def convert_pdf_to_images(source_dir, output_dir):
    """
    Convert all PDFs in the source directory (and subdirectories) to images.
    The images are saved in a folder structure that mirrors the source directory.
    """
    for root, _, files in os.walk(source_dir):
        for file in files:
            if file.endswith(".pdf"):
                pdf_path = os.path.join(root, file)
                relative_path = os.path.relpath(root, source_dir)  # Relative path from source_dir
                dest_folder = os.path.join(output_dir, relative_path, os.path.splitext(file)[0])  # Create subfolder for the PDF
                
                # Ensure the destination folder exists
                os.makedirs(dest_folder, exist_ok=True)
                
                try:
                    print(f"Converting: {pdf_path}")
                    # Convert PDF to images (all pages)
                    images = convert_from_path(pdf_path)
                    
                    # Save each page as an image
                    for page_number, image in enumerate(images, start=1):
                        image_file = os.path.join(dest_folder, f"page_{page_number}.png")
                        image.save(image_file, "PNG")
                        print(f"Saved: {image_file}")
                except Exception as e:
                    print(f"Error converting {pdf_path}: {e}")

# Define source and destination directories
source_directory = os.path.expanduser("~/Desktop/9618")
output_directory = os.path.expanduser("~/Desktop/converted_images")

# Run the conversion
convert_pdf_to_images(source_directory, output_directory)
