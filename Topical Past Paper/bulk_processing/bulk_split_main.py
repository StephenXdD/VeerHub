import fitz  # PyMuPDF
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

# Mapping for month abbreviations
mapping_dict = {
    'w': 'Oct_Nov',
    'm': 'Feb_March',
    's': 'May_June'
}

def find_question_number_in_area(page, search_area=75):
    """Searches for question numbers within the leftmost search area of the page."""
    rect = fitz.Rect(0, 0, search_area, page.rect.height)
    text = page.get_text("text", clip=rect).strip()
    match = re.match(r"^(\d+)\s", text)  # Matches a number at the start of the line followed by a space
    if match:
        question_number = int(match.group(1))
        logger.debug(f"Detected question number: {question_number} on page.")
        return question_number
    return None

def split_pdf_into_questions(input_pdf_path, output_dir, max_questions=12):
    """Splits the PDF into separate files by question, up to max_questions."""
    try:
        # Open the input PDF
        pdf_document = fitz.open(input_pdf_path)

        question_start_page = None
        current_question = 1
        saved_questions = set()  # Track saved question numbers

        for page_number in range(len(pdf_document)):
            if current_question > max_questions:
                break  # Stop if maximum number of questions reached

            page = pdf_document[page_number]

            # Search left margin for question number
            detected_question = find_question_number_in_area(page)

            # If we find a new question number and it's not a duplicate
            if detected_question is not None and detected_question not in saved_questions:
                if question_start_page is not None:
                    # Save the previous question's pages
                    save_question_pdf(pdf_document, question_start_page, page_number - 1, current_question, output_dir)
                    saved_questions.add(current_question)
                    current_question += 1

                # Set the start page for the current question
                question_start_page = page_number

        # Save the final question if it hasn't been saved
        if question_start_page is not None and current_question not in saved_questions:
            save_question_pdf(pdf_document, question_start_page, len(pdf_document) - 1, current_question, output_dir)
            saved_questions.add(current_question)

        pdf_document.close()

        logger.info(f"Questions saved for {input_pdf_path}: {sorted(saved_questions)}")

    except Exception as e:
        logger.error(f"Error processing PDF {input_pdf_path}: {e}", exc_info=True)

def save_question_pdf(pdf_document, start_page, end_page, question_number, output_dir):
    """Saves the specified pages as a separate PDF file for each question."""
    try:
        pdf_writer = fitz.open()
        for page_index in range(start_page, end_page + 1):
            pdf_writer.insert_pdf(pdf_document, from_page=page_index, to_page=page_index)

        output_pdf_path = os.path.join(output_dir, f"{question_number}.pdf")
        os.makedirs(output_dir, exist_ok=True)

        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        logger.info(f"Created: {output_pdf_path}")
    except Exception as e:
        logger.error(f"Error saving question PDF {question_number} to {output_dir}: {e}", exc_info=True)

def process_pdf_folder(input_folder, output_base_folder):
    """Processes all PDF files in a folder and splits them into questions."""
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            # Updated regex to match both `_qp_` and `_ms_`
            match = re.match(r"(\d{4})_([wms])(\d{2})_(qp|ms)_(\d{1,2})_cleaned", filename)
            if match:
                subject_code = match.group(1)
                mapping_code = match.group(2)
                year_suffix = match.group(3)
                paper_type = match.group(4)  # qp or ms
                paper_number = match.group(5)

                # Derive the full year
                if len(year_suffix) == 2:
                    if int(year_suffix) >= 15:
                        year = f"20{year_suffix}"
                    else:
                        year = f"20{year_suffix}"
                else:
                    year = year_suffix

                mapping = mapping_dict.get(mapping_code, "Unknown_Mapping")
                output_dir = os.path.join(output_base_folder, subject_code, year, mapping, paper_type, paper_number)

                input_pdf_path = os.path.join(input_folder, filename)
                split_pdf_into_questions(input_pdf_path, output_dir)
            else:
                logger.warning(f"Filename format not recognized: {filename}")

# Example usage
input_folder = "output_cleaned"  # Adjust to your input folder path
output_base_folder = "output_questions"  # Adjust to your output folder path

process_pdf_folder(input_folder, output_base_folder)
