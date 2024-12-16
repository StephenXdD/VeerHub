import os
import fitz  # PyMuPDF
import re


def increment_question_number(question_number):
    match = re.match(r"(\d+)(\([a-zA-Z]\))?", question_number)
    if match:
        base_number = int(match.group(1))  # The numeric part of the question
        return str(base_number + 1)  # Return the next number as a string
    return str(int(question_number) + 1)  # Increment if it's just a number


def crop_pdf(input_pdf_path, output_pdf_path):
    file_name = os.path.basename(input_pdf_path).split('.')[0]
    question_number = file_name  # Extract question number from the filename

    doc = fitz.open(input_pdf_path)

    # Define initial crop bounds
    left_crop = None
    right_crop = None

    # Define the search region for the first and last pages
    page_width = doc[0].rect.width
    page_height = doc[0].rect.height
    search_rect = fitz.Rect(0, page_height - 100, page_width, page_height)

    # Check for a single-page PDF
    is_single_page = doc.page_count == 1

    # Search for the current question on the first page (or only page)
    current_question_rects = None
    current_question_patterns = [f"{question_number}(a)", f"{question_number}(i)", question_number]
    
    for pattern in current_question_patterns:
        current_question_rects = doc[0].search_for(pattern, clip=search_rect)
        if current_question_rects:
            print(f"Found current question {pattern} on page 1.")
            left_crop = max(0, current_question_rects[0][0] - 5)  # Add safety margin to the left
            left_crop -= 5  # Move the left crop 5 points to the right to ensure a margin
            break  # Exit the loop if we find the pattern

    # If we found the current question, search for the next one
    if left_crop is not None:
        next_question = increment_question_number(question_number)
        next_question_patterns = [f"{next_question}(i)", f"{next_question}(a)", next_question]
        for pattern in next_question_patterns:
            next_question_rects = doc[-1].search_for(pattern, clip=search_rect)
            if next_question_rects:
                print(f"Found next question {pattern} on the last page.")
                right_crop = max(0, next_question_rects[0][0] - 35)  # Ensure right crop is non-negative
                right_crop -= 5  # Add a margin of 5 points to the right crop
                break

    # Validate cropping bounds
    if left_crop is not None and left_crop >= page_width:
        left_crop = None
    if right_crop is not None and right_crop <= 0:
        right_crop = None

    # Create a new PDF with adjusted cropping
    cropped_pdf = fitz.open()
    for page_num in range(doc.page_count):
        page = doc[page_num]
        cropped_page = cropped_pdf.new_page(width=page_width, height=page_height)

        # Determine cropping for the current page
        if is_single_page:
            # Apply both left and right crops on the single page
            if left_crop is not None and right_crop is not None:
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, right_crop - left_crop, page_height),
                    doc,
                    page_num,
                    clip=fitz.Rect(left_crop, 0, right_crop, page_height),
                )
            elif left_crop is not None:
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, page_width - left_crop, page_height),
                    doc,
                    page_num,
                    clip=fitz.Rect(left_crop, 0, page_width, page_height),
                )
            elif right_crop is not None:
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, right_crop, page_height),
                    doc,
                    page_num,
                    clip=fitz.Rect(0, 0, right_crop, page_height),
                )
            else:
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, page_width, page_height), doc, page_num
                )
        else:
            # Apply cropping for multi-page PDFs
            if page_num == 0 and left_crop is not None:
                # Apply left crop only to the first page
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, page_width - left_crop, page_height),
                    doc,
                    page_num,
                    clip=fitz.Rect(left_crop, 0, page_width, page_height),
                )
            elif page_num == doc.page_count - 1 and right_crop is not None:
                # Apply right crop only to the last page
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, right_crop, page_height),
                    doc,
                    page_num,
                    clip=fitz.Rect(0, 0, right_crop, page_height),
                )
            else:
                # Leave other pages unchanged
                cropped_page.show_pdf_page(
                    fitz.Rect(0, 0, page_width, page_height), doc, page_num
                )

    # Save the cropped PDF
    cropped_pdf.save(output_pdf_path)
    cropped_pdf.close()
    doc.close()


def process_pdfs(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for filename in files:
            if filename.endswith(".pdf"):
                input_pdf_path = os.path.join(root, filename)
                relative_path = os.path.relpath(root, input_folder)
                output_dir = os.path.join(output_folder, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                output_pdf_path = os.path.join(output_dir, filename)
                crop_pdf(input_pdf_path, output_pdf_path)


# Example usage:
input_folder = "output_questions"  # Folder containing PDFs
output_folder = "cropped_questions"  # Folder for saving cropped PDFs
process_pdfs(input_folder, output_folder)
