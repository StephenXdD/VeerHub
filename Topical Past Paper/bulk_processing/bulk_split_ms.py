import fitz  # PyMuPDF
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Mapping for session abbreviations
session_mapping = {
    "w": "Oct_Nov",
    "m": "Feb_March",
    "s": "May_June"
}

def find_all_questions_in_page(page):
    """
    Finds all questions and subquestions (e.g., '1(a)', '2(a)', ..., '5(k)') on the entire page.
    Returns a list of detected questions and the text of the page.
    """
    text = page.get_text("text").strip()  # Extract the entire page text
    matches = re.findall(r"(\d+\([a-k]\))", text)  # Match patterns like '1(a)', '2(b)', etc.
    return list(matches)

def split_pdf_by_questions(input_pdf_path, output_dir, max_questions=5):
    """
    Splits a PDF into separate files by questions like '1(a)', '2(a)', ..., '5(k)'.
    """
    pdf_document = fitz.open(input_pdf_path)
    total_pages = len(pdf_document)

    # Initialize a dictionary to track pages for each question
    question_pages = {f"{i}": [] for i in range(1, max_questions + 1)}

    # Find all pages containing each question and its subquestions
    for page_number in range(total_pages):
        page = pdf_document[page_number]
        detected_questions = find_all_questions_in_page(page)

        # Add this page to all the questions it contains
        for question in detected_questions:
            question_number = question.split("(")[0]
            if question_number in question_pages:
                question_pages[question_number].append(page_number)

    # Save the PDFs for each question
    for question_number, pages in question_pages.items():
        if not pages:
            continue  # Skip if no pages found for this question

        # Deduplicate pages (within this question only)
        pages = list(sorted(set(pages)))

        # Include all detected pages for the question, even if shared with others
        save_question_pdf(pdf_document, pages, question_number, output_dir)

    pdf_document.close()
    logger.info(f"Finished splitting PDF: {input_pdf_path}")


def save_question_pdf(pdf_document, pages, question, output_dir):
    """
    Saves the specified pages as a separate PDF for the given question.
    """
    pdf_writer = fitz.open()
    for page_number in pages:
        pdf_writer.insert_pdf(pdf_document, from_page=page_number, to_page=page_number)

    # Construct the output PDF path
    output_pdf_path = os.path.join(output_dir, f"{int(question)}.pdf")  # Save as 1.pdf, 2.pdf, etc.

    if len(pages) > 0:
        os.makedirs(output_dir, exist_ok=True)
        pdf_writer.save(output_pdf_path)
        logger.info(f"Created PDF for Question {question}: {output_pdf_path}")
    else:
        logger.warning(f"No pages found for Question {question}, skipping.")

    pdf_writer.close()


def process_pdf_folder(input_folder, output_base_folder):
    """
    Processes all PDF files in a folder and splits them into questions with a structured hierarchy.
    """
    for filename in os.listdir(input_folder):
        if filename.endswith(".pdf"):
            # Parse the filename to extract metadata
            match = re.match(r"(\d{4})_([wms])(\d{2})_(qp|ms)_(\d{1,2})_cleaned", filename)
            if match:
                subject_code = match.group(1)
                session_code = match.group(2)
                year_suffix = match.group(3)
                paper_type = match.group(4)
                paper_number = match.group(5)

                # Derive full year and session mapping
                year = f"20{year_suffix}" if len(year_suffix) == 2 else year_suffix
                session = session_mapping.get(session_code, "Unknown_Session")

                # Construct the output directory structure
                output_dir = os.path.join(
                    output_base_folder,
                    subject_code,
                    year,
                    session,
                    paper_type,
                    paper_number
                )

                input_pdf_path = os.path.join(input_folder, filename)
                split_pdf_by_questions(input_pdf_path, output_dir)
            else:
                logger.warning(f"Filename format not recognized: {filename}")

# Example usage
input_folder = "output_cleaned"  # Path to the input folder
output_base_folder = "output_questions"  # Base path for the output

process_pdf_folder(input_folder, output_base_folder)
