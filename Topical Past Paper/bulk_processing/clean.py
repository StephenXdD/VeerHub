import fitz  # PyMuPDF
import os

def remove_top_bottom_content(input_pdf, output_pdf, top_margin=50, bottom_margin=50):
    pdf_document = fitz.open(input_pdf)

    for page in pdf_document:
        # Define the area to be kept (remove content from top and bottom margins)
        rect = page.rect
        crop_rect = fitz.Rect(0, top_margin, rect.width, rect.height - bottom_margin)
        
        # Set the crop area to remove top and bottom content
        page.set_cropbox(crop_rect)
        
    pdf_document.save(output_pdf)
    pdf_document.close()

def process_all_pdfs_in_folder(input_folder, output_folder, top_margin=50, bottom_margin=50):
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pdf"):
            input_pdf_path = os.path.join(input_folder, file_name)
            output_pdf_path = os.path.join(output_folder, file_name)  # Save with the same name

            remove_top_bottom_content(input_pdf_path, output_pdf_path, top_margin, bottom_margin)
            print(f"Processed: {file_name}")

# Example usage
input_folder = "output_cleaned"  # Path to your folder containing PDFs
output_folder = "cleaned_pdfs"  # Path to save the processed PDFs
process_all_pdfs_in_folder(input_folder, output_folder)
