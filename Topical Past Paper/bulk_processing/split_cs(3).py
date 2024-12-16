import fitz  # PyMuPDF
import os
import re
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

def find_subquestion_labels_in_area(page, search_start=88, search_end=107):
    """Searches for subquestion labels like (i), (ii), (iii), etc. within the specified area of the page."""
    rect = fitz.Rect(search_start, 0, search_end, page.rect.height)
    text = page.get_text("text", clip=rect).strip()

    # Match patterns like (i), (ii), (iii), etc.
    labels = re.findall(r"\((ii?|iii?)\)", text)
    logger.debug(f"Found labels on page: {labels}")
    return labels

def split_pdf_into_subquestions(input_pdf_path, output_dir, max_subquestions=12):
    """Splits the PDF into separate files by subquestion (i), (ii), (iii), etc., up to max_subquestions."""
    try:
        # Open the input PDF
        pdf_document = fitz.open(input_pdf_path)

        saved_subquestions = set()  # Track saved subquestion labels
        subquestions_found = False  # Flag to track if any subquestions are found

        for page_number in range(len(pdf_document)):
            if len(saved_subquestions) >= max_subquestions:
                break  # Stop if maximum number of subquestions reached

            page = pdf_document[page_number]

            # Search for subquestion labels (i), (ii), (iii), etc.
            detected_labels = find_subquestion_labels_in_area(page)

            for label in detected_labels:
                if label not in saved_subquestions:
                    # Save the current page immediately for this subquestion label
                    save_subquestion_pdf(pdf_document, page_number, page_number, label, input_pdf_path, output_dir)
                    saved_subquestions.add(label)
                    subquestions_found = True  # Mark that we found subquestions

        pdf_document.close()

        if not subquestions_found:
            # If no subquestions were found, save the same file without any changes
            save_same_pdf(input_pdf_path, output_dir)

        logger.info(f"Subquestions saved for {input_pdf_path}: {sorted(saved_subquestions)}")

    except Exception as e:
        logger.error(f"Error processing PDF {input_pdf_path}: {e}", exc_info=True)

def save_subquestion_pdf(pdf_document, start_page, end_page, subquestion_label, input_pdf_path, output_dir):
    """Saves the specified page as a separate PDF file for each subquestion."""
    try:
        pdf_writer = fitz.open()
        for page_index in range(start_page, end_page + 1):
            pdf_writer.insert_pdf(pdf_document, from_page=page_index, to_page=page_index)

        # Use the original filename and append the subquestion label (i), (ii), etc.
        base_filename = os.path.basename(input_pdf_path)
        file_name_without_extension, file_extension = os.path.splitext(base_filename)
        output_pdf_path = os.path.join(output_dir, f"{file_name_without_extension}({subquestion_label}){file_extension}")

        os.makedirs(output_dir, exist_ok=True)

        pdf_writer.save(output_pdf_path)
        pdf_writer.close()
        logger.info(f"Created: {output_pdf_path}")
    except Exception as e:
        logger.error(f"Error saving subquestion PDF ({subquestion_label}) to {output_dir}: {e}", exc_info=True)

def save_same_pdf(input_pdf_path, output_dir):
    """Saves the same PDF without any changes."""
    try:
        # Open the input PDF and save it as-is
        pdf_document = fitz.open(input_pdf_path)

        # Use the original filename to save the same file
        base_filename = os.path.basename(input_pdf_path)
        file_name_without_extension, file_extension = os.path.splitext(base_filename)
        output_pdf_path = os.path.join(output_dir, f"{file_name_without_extension}{file_extension}")

        os.makedirs(output_dir, exist_ok=True)

        pdf_document.save(output_pdf_path)
        pdf_document.close()
        logger.info(f"Created: {output_pdf_path}")
    except Exception as e:
        logger.error(f"Error saving the same PDF to {output_dir}: {e}", exc_info=True)

def process_pdf_folder(input_folder, output_base_folder):
    """Processes all PDF files in a folder and splits them into subquestions."""
    for root, dirs, files in os.walk(input_folder):  # Walk through all directories
        for filename in files:
            if filename.endswith(".pdf"):
                input_pdf_path = os.path.join(root, filename)

                # Get the relative path of the file within the input folder
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_base_folder, relative_path)

                split_pdf_into_subquestions(input_pdf_path, output_dir)

# Example usage
input_folder = "output_questions(1)"  # Input folder path
output_base_folder = "output_questions(2)"  # Output folder path

# Ensure the output base folder exists
os.makedirs(output_base_folder, exist_ok=True)

process_pdf_folder(input_folder, output_base_folder)
