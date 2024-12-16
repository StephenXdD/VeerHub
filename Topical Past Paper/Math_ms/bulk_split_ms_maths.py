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

def extract_all_questions_after_guidance(page_text):
    """
    Extracts all question numbers after every instance of 'Guidance' in the given page text.
    Returns a list of question numbers in the order they appear.
    """
    matches = re.findall(r"Guidance\s*(.*)", page_text)
    question_numbers = []
    for match in matches:
        question_match = re.match(r"(\d+(\([a-zA-Z]+\)|\([ivx]+\))?)", match.strip())
        if question_match:
            question_numbers.append(question_match.group(1))
    return question_numbers

def get_main_question_number(question):
    """
    Extracts the main question number (e.g., '1' from '1', '1(a)', '2(i)', etc.)
    """
    return re.match(r"(\d+)", question).group(1)

def save_pages_to_pdf(pdf_document, pages, question, output_dir):
    """
    Save the specified pages from the given PDF document into a new PDF.
    """
    try:
        pdf_writer = fitz.open()
        for page_number in pages:
            pdf_writer.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

        output_pdf_path = os.path.join(output_dir, f"{question}.pdf")
        os.makedirs(output_dir, exist_ok=True)
        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        logger.info(f"Saved: {output_pdf_path}")
    except Exception as e:
        logger.error(f"Error saving question PDF {question} to {output_dir}: {e}", exc_info=True)

def split_pdf_by_questions(input_pdf_path, output_dir):
    """
    Splits a PDF into multiple PDFs based on questions identified after 'Guidance'.
    Handles multiple 'Guidance' instances on the same page and groups sub-questions together.
    """
    pdf_document = fitz.open(input_pdf_path)
    total_pages = pdf_document.page_count

    current_question = None
    current_pages = []

    for page_number in range(total_pages):
        page = pdf_document[page_number]
        text = page.get_text("text")  # Extract text from the page
        questions_on_page = extract_all_questions_after_guidance(text)

        if questions_on_page:
            for question_number in questions_on_page:
                if current_question is None:
                    current_question = question_number
                    current_pages.append(page_number)
                else:
                    current_main_question = get_main_question_number(current_question)
                    next_main_question = get_main_question_number(question_number)

                    if next_main_question == current_main_question:
                        if page_number not in current_pages:
                            current_pages.append(page_number)
                    else:
                        save_pages_to_pdf(pdf_document, current_pages, current_question, output_dir)
                        current_question = question_number
                        current_pages = [page_number]
        else:
            if current_question:
                current_pages.append(page_number)

    if current_question and current_pages:
        save_pages_to_pdf(pdf_document, current_pages, current_question, output_dir)

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