import os
import fitz  # PyMuPDF

def draw_green_line_in_pdf(pdf_path, output_path, offset_from_bottom=1):
    # Open the existing PDF
    pdf_document = fitz.open(pdf_path)
    
    # Loop through each page in the PDF
    for page_num in range(pdf_document.page_count):
        page = pdf_document.load_page(page_num)
        
        # Calculate the position for the green line from the bottom
        y_position = page.rect.height - offset_from_bottom
        
        # Define the start and end points of the line
        start_point = (0, y_position)  # Starting point (left, top)
        end_point = (page.rect.width, y_position)  # Ending point (right, top)
        
        # Draw a green line
        page.draw_line(start_point, end_point, color=(0, 1, 0), width=2)
    
    # Save the modified PDF to the output path
    pdf_document.save(output_path)

def process_pdfs_in_folder(input_folder, output_folder):
    # Get a list of all PDFs in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            
            # Draw the green line and save the modified PDF
            draw_green_line_in_pdf(pdf_path, output_path)

# Set the input and output folder paths
input_folder = "output_questions"
output_folder = "drawn_pdfs"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all PDFs in the input folder
process_pdfs_in_folder(input_folder, output_folder)
