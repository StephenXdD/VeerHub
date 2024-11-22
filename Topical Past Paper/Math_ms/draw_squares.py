import fitz  # PyMuPDF

def draw_square_on_pdf(input_pdf, output_pdf, square_size=75):
    # Open the PDF
    doc = fitz.open(input_pdf)
    
    # Loop through each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)
        page_width = page.rect.width
        page_height = page.rect.height
        
        # Calculate the position for the top-right corner
        x0 = 0
        y0 = 0
        x1 = square_size
        y1 = square_size
        
        # Define the rectangle for the square
        rect = fitz.Rect(x0, y0, x1, y1)
        
        # Draw the rectangle with a red border
        page.draw_rect(rect, color=(1, 0, 0), width=1)  # Red border, 1 point width
        
    # Save the modified PDF
    doc.save(output_pdf)
    doc.close()
    
    print(f"PDF with squares saved as {output_pdf}")

# Input and output PDF paths
input_pdf = "2(i).pdf"  # Path to the input PDF
output_pdf = "output_with_square(1).pdf"  # Path to save the output PDF

# Draw the square on the PDF
draw_square_on_pdf(input_pdf, output_pdf)
