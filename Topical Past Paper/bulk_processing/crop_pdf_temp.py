import fitz  # PyMuPDF
import os
import re

def mark_and_crop_two_areas(input_dir, output_dir, safety_margin=5):
    """
    Processes each PDF page by cropping content based on the current and next question positions.
    The top crop box removes content above the current question, and the bottom crop box removes content up to the start of the next question.
    
    Parameters:
    - input_dir (str): Directory containing the question PDFs.
    - output_dir (str): Directory to save the cropped PDFs.
    - safety_margin (int): Pixels to subtract from the top crop position for a safety margin.
    """
    not_found_files = []  # List to keep track of files where the question was not found
    
    try:
        # Ensure the output directory exists
        os.makedirs(output_dir, exist_ok=True)

        # Loop through all directories and files in the input directory
        for root, dirs, files in os.walk(input_dir):
            for filename in files:
                if filename.endswith(".pdf"):
                    # Extract the question number from the filename (e.g., "1.pdf" -> "1")
                    question_number = filename.split(".")[0]
                    next_question_number = str(int(question_number) + 1)  # Find the next question number

                    input_path = os.path.join(root, filename)
                    pdf_document = fitz.open(input_path)

                    question_found = False  # Flag to track if the question is found

                    # Loop through each page and process
                    for page_num in range(pdf_document.page_count):
                        page = pdf_document[page_num]
                        media_box = page.rect  # Get the page's MediaBox

                        # Define the region to search for questions (first 70 units from the left, full page height)
                        clipping_rect = fitz.Rect(0, 0, 60, media_box.height)

                        # Find the current question number within the clipping area (70 units from the left)
                        search_pattern = rf"\b{question_number}\b(?!\.\d)"
                        match = re.search(search_pattern, page.get_text("text", clip=clipping_rect))
                        current_top_y = None  # Initialize for safety
                        if match:
                            current_rect = page.search_for(str(question_number), clip=clipping_rect)
                            if current_rect:
                                current_top_y = max(0, min(current_rect[0].y0, media_box.height))
                                # Apply the safety margin (subtract from the top crop position)
                                current_top_y = max(0, current_top_y - safety_margin)
                                print(f"Top crop box set above question {question_number} in {filename}, page {page_num + 1}")
                            else:
                                print(f"Could not find question {question_number} position in {filename}, page {page_num + 1}")
                        else:
                            print(f"Question number {question_number} not found in {filename}, page {page_num + 1}")

                        # Now, find the next question number to set the bottom crop
                        next_question_top_y = None  # This will store the top Y position of the next question
                        search_pattern_next = rf"\b{next_question_number}\b(?!\.\d)"
                        next_match = re.search(search_pattern_next, page.get_text("text", clip=clipping_rect))

                        if next_match:
                            next_rect = page.search_for(str(next_question_number), clip=clipping_rect)
                            if next_rect:
                                next_question_top_y = next_rect[0].y0  # Get the Y position of the next question
                                print(f"Next question '{next_question_number}' found at: {next_rect[0]}")

                        # If we found the next question, set the bottom crop box to just before it
                        if next_question_top_y is not None:
                            bottom_crop_y = next_question_top_y  # Set the bottom crop to the start of the next question
                        else:
                            bottom_crop_y = media_box.height  # If no next question, set to the end of the page

                        # Ensure the crop box coordinates are within the page's MediaBox
                        if current_top_y is not None and bottom_crop_y is not None:
                            current_top_y = max(current_top_y, 0)  # Ensures it is not less than 0
                            bottom_crop_y = min(bottom_crop_y, media_box.height)  # Ensures it does not exceed page height

                            # Apply the crop box only if the crop area is valid
                            if current_top_y < bottom_crop_y:
                                page.set_cropbox(fitz.Rect(0, current_top_y, media_box.width, bottom_crop_y))
                                print(f"Applied crop boxes on page {page_num + 1} of {filename}")
                                question_found = True  # Mark the question as found
                            else:
                                print(f"Skipping invalid crop box (current_top_y: {current_top_y}, bottom_crop_y: {bottom_crop_y}) on page {page_num + 1} of {filename}")
                    
                    # If the question was not found in the PDF, add it to the list of not found files
                    if not question_found:
                        print(f"Question {question_number} not found in {filename}, retrying with 85 units from the left.")
                        
                        # Retry the check with 85 units from the left
                        for page_num in range(pdf_document.page_count):
                            page = pdf_document[page_num]
                            media_box = page.rect  # Get the page's MediaBox

                            # Define the region to search for questions (first 85 units from the left, full page height)
                            clipping_rect = fitz.Rect(0, 0, 85, media_box.height)

                            # Find the current question number within the clipping area (85 units from the left)
                            match = re.search(search_pattern, page.get_text("text", clip=clipping_rect))
                            current_top_y = None  # Initialize for safety
                            if match:
                                current_rect = page.search_for(str(question_number), clip=clipping_rect)
                                if current_rect:
                                    current_top_y = max(0, min(current_rect[0].y0, media_box.height))
                                    # Apply the safety margin (subtract from the top crop position)
                                    current_top_y = max(0, current_top_y - safety_margin)
                                    print(f"Top crop box set above question {question_number} in {filename}, page {page_num + 1}")
                                else:
                                    print(f"Could not find question {question_number} position in {filename}, page {page_num + 1}")
                            else:
                                print(f"Question number {question_number} not found in {filename}, page {page_num + 1}")

                            # Now, find the next question number to set the bottom crop
                            next_question_top_y = None  # This will store the top Y position of the next question
                            next_match = re.search(search_pattern_next, page.get_text("text", clip=clipping_rect))

                            if next_match:
                                next_rect = page.search_for(str(next_question_number), clip=clipping_rect)
                                if next_rect:
                                    next_question_top_y = next_rect[0].y0  # Get the Y position of the next question
                                    print(f"Next question '{next_question_number}' found at: {next_rect[0]}")

                            # If we found the next question, set the bottom crop box to just before it
                            if next_question_top_y is not None:
                                bottom_crop_y = next_question_top_y  # Set the bottom crop to the start of the next question
                            else:
                                bottom_crop_y = media_box.height  # If no next question, set to the end of the page

                            # Ensure the crop box coordinates are within the page's MediaBox
                            if current_top_y is not None and bottom_crop_y is not None:
                                current_top_y = max(current_top_y, 0)  # Ensures it is not less than 0
                                bottom_crop_y = min(bottom_crop_y, media_box.height)  # Ensures it does not exceed page height

                                # Apply the crop box only if the crop area is valid
                                if current_top_y < bottom_crop_y:
                                    page.set_cropbox(fitz.Rect(0, current_top_y, media_box.width, bottom_crop_y))
                                    print(f"Applied crop boxes on page {page_num + 1} of {filename}")
                                    question_found = True  # Mark the question as found
                                else:
                                    print(f"Skipping invalid crop box (current_top_y: {current_top_y}, bottom_crop_y: {bottom_crop_y}) on page {page_num + 1} of {filename}")

                    # If the question was not found in the PDF after both attempts, add it to the list of not found files
                    if not question_found:
                        not_found_files.append(input_path)

                    # Save the updated PDF in the corresponding output directory
                    relative_path = os.path.relpath(root, input_dir)  # Get subdirectory relative to input
                    output_subdir = os.path.join(output_dir, relative_path)  # Create output subdirectory structure
                    os.makedirs(output_subdir, exist_ok=True)  # Ensure the subdirectory exists

                    output_path = os.path.join(output_subdir, filename)
                    pdf_document.save(output_path)
                    print(f"Processed {filename} saved as {output_path}")
                    
                    # Close the document
                    pdf_document.close()

        # Print the full paths of all files where the question was not found
        if not_found_files:
            print("\nThe following files did not contain the specified question:")
            for file in not_found_files:
                print(file)
        else:
            print("\nAll questions were found and cropped successfully.")

    except Exception as e:
        print("Error while processing PDFs:", e)

# Usage example
input_directory = os.path.expanduser("output_questions")  # Path to the input folder (on Desktop)
output_directory = os.path.expanduser("cropped_questions")  # Path to the output folder (on Desktop)
mark_and_crop_two_areas(input_directory, output_directory, safety_margin=5)  # Set safety margin to 5 pixels