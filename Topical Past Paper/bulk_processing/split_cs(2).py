import fitz  # PyMuPDF
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def find_question_labels_in_area(page, search_start=70, search_end=88):
    """Searches for question labels like (a), (b), (c), etc. within the specified area of the page."""
    rect = fitz.Rect(search_start, 0, search_end, page.rect.height)
    text = page.get_text("text", clip=rect).strip()
    
    # Match patterns like (a), (b), (c), etc.
    labels = re.findall(r"\((\w)\)", text)
    logger.debug(f"Found labels on page: {labels}")
    return labels

def split_pdf_into_questions(input_pdf_path, output_dir, max_questions=12):
    """Splits the PDF into separate files by question, up to max_questions."""
    try:
        # Open the input PDF
        pdf_document = fitz.open(input_pdf_path)

        saved_questions = set()  # Track saved question labels
        question_ranges = {}  # Track the range of pages for each subquestion

        last_found_label = None  # To track the last found subquestion
        start_page = None  # To track the start page for a subquestion
        end_page = None  # To track the end page for a subquestion

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]

            # Search for question labels (a), (b), (c), etc.
            detected_labels = find_question_labels_in_area(page)

            # If there is any detected label (e.g., (a), (b), (c)), process it
            if detected_labels:
                for label in detected_labels:
                    if label not in saved_questions:
                        # If we were previously tracking a label, save its range of pages
                        if last_found_label is not None and start_page is not None:
                            save_question_pdf(pdf_document, start_page, end_page, last_found_label, input_pdf_path, output_dir)
                            saved_questions.add(last_found_label)

                        # Start a new range for the current subquestion
                        last_found_label = label
                        start_page = page_number
                        end_page = page_number

            # If no label is detected but we are tracking a question, keep extending its range
            if last_found_label is not None and detected_labels == []:
                # Keep extending the end page until we find a new label
                end_page = page_number

        # After processing all pages, save the last found question range
        if last_found_label is not None and start_page is not None:
            save_question_pdf(pdf_document, start_page, end_page, last_found_label, input_pdf_path, output_dir)

        pdf_document.close()

        logger.info(f"Questions saved for {input_pdf_path}: {sorted(saved_questions)}")

    except Exception as e:
        logger.error(f"Error processing PDF {input_pdf_path}: {e}", exc_info=True)

def save_question_pdf(pdf_document, start_page, end_page, question_label, input_pdf_path, output_dir):
    """Saves the specified pages as a separate PDF file for each question."""
    try:
        pdf_writer = fitz.open()

        # Insert the collected pages into the PDF writer
        for page_index in range(start_page, end_page + 1):
            pdf_writer.insert_pdf(pdf_document, from_page=page_index, to_page=page_index)

        # Use the original filename and append the question label (a), (b), etc.
        base_filename = os.path.basename(input_pdf_path)
        file_name_without_extension, file_extension = os.path.splitext(base_filename)
        output_pdf_path = os.path.join(output_dir, f"{file_name_without_extension}({question_label}){file_extension}")
        
        os.makedirs(output_dir, exist_ok=True)

        # Save the collected pages as a new PDF
        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        logger.info(f"Created: {output_pdf_path}")
    except Exception as e:
        logger.error(f"Error saving question PDF ({question_label}) to {output_dir}: {e}", exc_info=True)

def process_pdf_folder(input_folder, output_base_folder):
    """Processes all PDF files in a folder and splits them into questions."""
    for root, dirs, files in os.walk(input_folder):  # Walk through all directories
        for filename in files:
            if filename.endswith(".pdf"):
                input_pdf_path = os.path.join(root, filename)

                # Get the relative path of the file within the input folder
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_base_folder, relative_path)

                split_pdf_into_questions(input_pdf_path, output_dir)

# Example usage
input_folder = "output_questions"  # Input folder path
output_base_folder = "output_questions(1)"  # Output folder path

# Ensure the output base folder exists
os.makedirs(output_base_folder, exist_ok=True)

process_pdf_folder(input_folder, output_base_folder)
