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

def extract_questions_on_page(page_text, left_margin_threshold=80):
    """
    Extracts all question numbers on the page within 70 points of the left margin.
    Returns a list of question numbers in the order they appear.
    """
    question_numbers = []

    for block in page_text:
        x0, _, _, _, text = block[:5]
        if x0 <= left_margin_threshold:  # Questions near the left margin
            # Match patterns like '1', '1(a)', '1(a)(i)', etc.
            question_match = re.match(r"(\d+(\([a-zA-Z]+\))*(\([ivx]+\))*)", text.strip())
            if question_match:
                question_numbers.append(question_match.group(1))
    return question_numbers

def save_page_as_question(pdf_document, page_number, question, output_dir):
    """
    Save a specific page of a PDF as a separate file with the given question number as the filename.
    """
    try:
        pdf_writer = fitz.open()
        pdf_writer.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)
        output_pdf_path = os.path.join(output_dir, f"{question}.pdf")
        os.makedirs(output_dir, exist_ok=True)
        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        logger.info(f"Saved: {output_pdf_path}")
    except Exception as e:
        logger.error(f"Error saving question PDF {question}: {e}", exc_info=True)

def split_pdf_by_questions(input_pdf_path, output_dir):
    """
    Splits a PDF into multiple PDFs based on questions identified within 70 points of the left margin.
    Saves each question individually.
    """
    pdf_document = fitz.open(input_pdf_path)
    total_pages = pdf_document.page_count

    for page_number in range(total_pages):
        page = pdf_document[page_number]
        text_blocks = page.get_text("blocks")  # Extract blocks of text
        questions_on_page = extract_questions_on_page(text_blocks)

        if questions_on_page:
            for question in questions_on_page:
                save_page_as_question(pdf_document, page_number, question, output_dir)

    pdf_document.close()
    logger.info(f"Finished splitting {input_pdf_path} into questions!")

def process_pdf_folder(input_folder, output_base_folder):
    """
    Processes all PDF files in a folder, splitting them into questions.
    """
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            match = re.match(r"(\d{4})_([wms])(\d{2})_ms_(\d{1,2})_cleaned\.pdf", filename, re.IGNORECASE)
            if match:
                subject_code = match.group(1)
                mapping_code = match.group(2).lower()
                year_suffix = match.group(3)
                paper_number = match.group(4)

                if mapping_code not in mapping_dict:
                    raise ValueError(f"Invalid mapping code '{mapping_code}' in file '{filename}'.")

                year = f"20{year_suffix}"
                mapping = mapping_dict[mapping_code]
                output_dir = os.path.join(output_base_folder, "ms", subject_code, year, mapping, paper_number)

                input_pdf_path = os.path.join(input_folder, filename)
                split_pdf_by_questions(input_pdf_path, output_dir)
            else:
                logger.warning(f"Filename format not recognized: {filename}")

# Example usage
input_folder = "cleaned_pdfs"  # Adjust to your input folder path
output_base_folder = "output_questions"  # Adjust to your output folder path

process_pdf_folder(input_folder, output_base_folder)
