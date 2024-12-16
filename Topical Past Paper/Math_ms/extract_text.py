import fitz  # PyMuPDF

def extract_and_print_page_range(pdf_path, start_page, end_page):
    """
    Extracts and prints text from a specified range of pages in a PDF file.

    Args:
        pdf_path (str): Path to the PDF file.
        start_page (int): The first page to extract (0-based index).
        end_page (int): The last page to extract (0-based index, exclusive).
    """
    try:
        # Open the PDF
        pdf_document = fitz.open(pdf_path)

        # Get the total number of pages
        total_pages = pdf_document.page_count

        # Ensure the range is within bounds
        if start_page < 0 or end_page > total_pages or start_page >= end_page:
            print("Invalid page range.")
            return

        # Iterate through the specified page range and extract text
        for page_number in range(start_page, end_page):
            page = pdf_document.load_page(page_number)
            page_text = page.get_text()

            # Print page number and text
            print(f"--- Page {page_number + 1} ---")
            print(page_text)
            print("\n")  # Separate pages with a newline

        pdf_document.close()

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
pdf_path = "1.pdf"  # Replace with the path to your PDF file

# Specify the page range (e.g., 0-4 for the first 5 pages, or 5-8 for pages 6-8)
start_page = 0  # 0-based index for the first page in the range
end_page = 1    # 0-based index, exclusive (i.e., up to but not including this page)

# Extract and print text from the specified range
extract_and_print_page_range(pdf_path, start_page, end_page)
