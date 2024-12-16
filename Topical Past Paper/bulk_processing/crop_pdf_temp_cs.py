import fitz  # PyMuPDF
import os

def get_next_subquestion_for_type(subquestion, subquestion_type):
    """Determines the next subquestion in sequence, based on the type (alphabetical or Roman)."""
    if subquestion_type == "alphabetical":
        alphabet_subquestions = {
            "(a)": "(b)", "(b)": "(c)", "(c)": "(d)", "(d)": "(e)", "(e)": "(f)"
        }
        return alphabet_subquestions.get(subquestion, None)
    
    elif subquestion_type == "roman":
        roman_numerals = {
            "(i)": "(ii)", "(ii)": "(iii)", "(iii)": "(iv)", "(iv)": "(v)", 
            "(v)": "(vi)", "(vi)": "(vii)", "(vii)": "(viii)"
        }
        return roman_numerals.get(subquestion, None)

    return None

def search_within_area(page, text, x_left, x_right, y_top, y_bottom):
    """Searches for text within a specified rectangular area."""
    search_area = fitz.Rect(x_left, y_top, x_right, y_bottom)
    matches = page.search_for(text, clip=search_area)
    return matches

def calculate_crop_points(page, main_question, alphabetical_subquestion, roman_subquestion, safety_margin=5):
    """Calculates the top and bottom crop points."""
    media_box = page.rect
    top_crop_y = 0
    bottom_crop_y = media_box.height
    
    next_alphabetical_subquestion = get_next_subquestion_for_type(alphabetical_subquestion, "alphabetical") if alphabetical_subquestion else None
    next_roman_subquestion = get_next_subquestion_for_type(roman_subquestion, "roman") if roman_subquestion else None
    
    # --- Top Crop Logic ---    
    if roman_subquestion:  # If there is a Roman subquestion
        if roman_subquestion != "(i)":  # Not "(i)", crop above the Roman subquestion
            match_top = page.search_for(roman_subquestion)
            if match_top:
                top_crop_y = max(0, match_top[0].y0 - safety_margin)
        else:  # If it is "(i)", check alphabetical subquestion
            if alphabetical_subquestion and alphabetical_subquestion != "(a)":  # Not "(a)", crop above the alphabetical subquestion
                match_top = page.search_for(alphabetical_subquestion)
                if match_top:
                    top_crop_y = max(0, match_top[0].y0 - safety_margin)
            elif alphabetical_subquestion == "(a)":  # Specifically "(a)", crop above the main question
                match_top = search_within_area(page, main_question, 0, 70, 0, media_box.height)
                if match_top:
                    top_crop_y = max(0, match_top[0].y0 - safety_margin)
    else:  # No Roman subquestion, check alphabetical subquestion
        if alphabetical_subquestion:
            if alphabetical_subquestion != "(a)":  # Not "(a)", crop above the alphabetical subquestion
                match_top = page.search_for(alphabetical_subquestion)
                if match_top:
                    top_crop_y = max(0, match_top[0].y0 - safety_margin)
            elif alphabetical_subquestion == "(a)":  # Specifically "(a)", crop above the main question
                match_top = search_within_area(page, main_question, 0, 70, 0, media_box.height)
                if match_top:
                    top_crop_y = max(0, match_top[0].y0 - safety_margin)

    # --- Bottom Crop Logic ---
    fallback_found = False
    last_text_y = 0  # Track the position of the last text found on the page

    # Check if next Roman subquestion exists
    if next_roman_subquestion:  
        match_bottom = page.search_for(next_roman_subquestion)
        if match_bottom:
            bottom_crop_y = match_bottom[0].y0  # Removed the safety margin here
            fallback_found = True

    # Check if next alphabetical subquestion exists
    if not fallback_found and next_alphabetical_subquestion:
        match_bottom = page.search_for(next_alphabetical_subquestion)
        if match_bottom:
            bottom_crop_y = match_bottom[0].y0  # Removed the safety margin here
            fallback_found = True

    # If neither is found, skip bottom crop
    if not fallback_found:
        if next_alphabetical_subquestion is None and next_roman_subquestion is None:
            print("Skipping bottom crop: neither next alphabetical nor Roman subquestion found.")
            bottom_crop_y = media_box.height  # Keep the bottom crop as the full height of the page

    # --- Fallback Logic for Bottom Crop ---
    if not fallback_found:
        text_blocks = page.get_text("dict")["blocks"]
        last_text_block = None
        for block in text_blocks:
            if "lines" in block:
                for line in block["lines"]:
                    for span in line["spans"]:
                        if not last_text_block or span["bbox"][1] > last_text_block[1]:
                            last_text_block = span["bbox"]
        if last_text_block:
            last_text_y = last_text_block[1]  # y1 of the last text block
            bottom_crop_y = last_text_y  # Removed the safety margin here

    # Ensure the crop box stays within the media box bounds
    top_crop_y = max(0, min(top_crop_y, media_box.height))
    bottom_crop_y = max(0, min(bottom_crop_y, media_box.height))

    return top_crop_y, bottom_crop_y

def apply_crop(page, top_crop_y, bottom_crop_y):
    """Applies the crop on the page."""
    media_box = page.rect
    if top_crop_y < bottom_crop_y:
        page.set_cropbox(fitz.Rect(0, top_crop_y, media_box.width, bottom_crop_y))
    else:
        print("Invalid crop dimensions. Skipping crop.")

def mark_and_crop_three_areas(input_dir, output_dir, safety_margin=5):
    """Main function to process all PDFs in the input directory and apply cropping logic."""
    try:
        os.makedirs(output_dir, exist_ok=True)

        for root, _, files in os.walk(input_dir):
            for filename in files:
                if filename.endswith(".pdf"):
                    # Parse filename to extract main and subquestions
                    question_number = filename.split(".")[0]
                    main_question = question_number.split("(")[0]  # Extract main question (e.g., "7")
                    subquestions = question_number.split("(")[1:] if "(" in question_number else []

                    # Initialize the subquestions as None
                    alphabetical_subquestion = f"({subquestions[0].strip(')')})" if len(subquestions) > 0 else None
                    roman_subquestion = f"({subquestions[1].strip(')')})" if len(subquestions) > 1 else None

                    input_path = os.path.join(root, filename)
                    pdf_document = fitz.open(input_path)

                    for page_num in range(pdf_document.page_count):
                        page = pdf_document[page_num]

                        # Calculate top and bottom crop points
                        top_crop_y, bottom_crop_y = calculate_crop_points(page, main_question, alphabetical_subquestion, roman_subquestion, safety_margin)

                        # For multi-page PDFs, apply top crop only on the first page and bottom crop on the last page
                        if pdf_document.page_count > 1:
                            # Apply top crop on the first page
                            if page_num == 0 and top_crop_y < page.rect.height:
                                apply_crop(page, top_crop_y, page.rect.height)

                            # Apply bottom crop on the last page
                            if page_num == pdf_document.page_count - 1 and bottom_crop_y < page.rect.height:
                                apply_crop(page, 0, bottom_crop_y)
                        else:
                            # For single-page PDFs, apply top and bottom crop normally
                            apply_crop(page, top_crop_y, bottom_crop_y)

                    # Save the cropped PDF
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)
                    output_path = os.path.join(output_subdir, filename)
                    pdf_document.save(output_path)
                    print(f"Processed {filename} saved as {output_path}")
                    pdf_document.close()

        print("Processing complete.")

    except Exception as e:
        print(f"Error processing PDFs: {e}")

# Example usage
input_dir = "output_questions(2)"  # Path to your input folder
output_dir = "output_cropped"      # Path to your output folder
mark_and_crop_three_areas(input_dir, output_dir)
