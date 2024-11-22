import sqlite3
import os
from docx import Document

def get_variant_from_month(month):
    # Map month abbreviation to variant code
    mapping = {'May/June': 's', 'Feb/March': 'm', 'Oct/Nov': 'w'}
    return mapping.get(month, '')

def map_variant(variant):
    # Map the value found in the database (variant) to the correct month variant abbreviation
    mapping = {'May/June': 's', 'Feb/March': 'm', 'Oct/Nov': 'w'}
    # If the variant is found in the mapping, return the mapped value
    return mapping.get(variant, variant)  # If not found, return as is (this case shouldn't happen if the data is consistent)

def reverse_map_variant(variant):
    # Reverse map the abbreviation back to the full month name
    reverse_mapping = {'m': 'Feb/March', 's': 'May/June', 'w': 'Oct/Nov'}
    return reverse_mapping.get(variant, variant)  # If not found, return as is

def get_file_path(subject_code, variant, year, paper_variant):
    # Convert year to string and then extract the last two digits for the file path
    return f"C:/Users/Dev Joshi/Desktop/Topical Past Paper/temp/cleaned_{subject_code}_{variant}{str(year)[-2:]}_ms_{paper_variant}.docx"

def extract_answer_from_docx(docx_path, question_number):
    # Open the Word document and extract the answer for the given question
    if not os.path.exists(docx_path):
        print(f"File not found: {docx_path}")
        return None
    
    # Load the docx file
    doc = Document(docx_path)
    
    # Search for the question number in the table and retrieve the answer
    for table in doc.tables:
        for row in table.rows:
            cells = row.cells
            # Assuming the first and third columns are Question, and second and fourth are Key
            if len(cells) >= 4:  # We need at least four columns: Question, Key, Question, Key
                question_text_1 = cells[0].text.strip()  # First Question
                answer_text_1 = cells[1].text.strip()  # First Key
                question_text_2 = cells[2].text.strip()  # Second Question
                answer_text_2 = cells[3].text.strip()  # Second Key
                
                # Match the question number (e.g., "1", "2", etc.) in the question columns
                if question_text_1.startswith(str(question_number)):
                    return answer_text_1
                elif question_text_2.startswith(str(question_number)):
                    return answer_text_2
    return None

def update_answer_in_db(db_path, subject_name="Economics"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Search for all rows where the subject_name is Physics
    cursor.execute("SELECT * FROM past_papers WHERE subject_name = ?", (subject_name,))
    rows = cursor.fetchall()
    
    for row in rows:
        subject_code = row[1]  # Assuming subject_code is in the 2nd column
        full_year = row[8]  # Full year from the VariantYear column (e.g., 2016, 2022)
        paper_variant = row[5]  # Assuming month is in the 6th column (e.g., "May/June")
        variant = row[6]  # Assuming Variant is in the 7th column (e.g., "May/June")
        question_number = row[10]  # Assuming question number is in the 12th column (e.g., 1, 2, etc.)
        
        # Immediately map the variant using the mapping function
        variant = map_variant(variant)
        
        # Generate the file path for the corresponding .docx file (use only last 2 digits of year)
        docx_path = get_file_path(subject_code, variant, full_year, paper_variant)
        
        # Extract the answer from the .docx file
        answer = extract_answer_from_docx(docx_path, question_number)
        
        if answer is not None:
            # Reverse map the variant back to the original form before updating the database
            original_variant = reverse_map_variant(variant)
            
            # Update the database using the full year and relevant columns for finding the correct row
            cursor.execute(""" 
                UPDATE past_papers 
                SET Answer = ?  
                WHERE subject_code = ? 
                AND variant = ? 
                AND year = ? 
                AND paper_variant = ? 
                AND question_number = ?  -- Add a condition to ensure we're updating the right row based on the question
            """, (answer, subject_code, original_variant, full_year, paper_variant, question_number))
            
            # Get the rowid of the updated row
            cursor.execute("SELECT rowid FROM past_papers WHERE subject_code = ? AND variant = ? AND year = ? AND paper_variant = ? AND question_number = ?", 
                           (subject_code, original_variant, full_year, paper_variant, question_number))
            row_id = cursor.fetchone()
            
            if row_id:  # Ensure row_id is not None before attempting to access it
                print(f"Updated answer for question {question_number} in {subject_name}: {answer} (Row ID: {row_id[0]})")
            else:
                print(f"No matching row found for question {question_number} in {subject_name}")
        else:
            print(f"Answer not found for question {question_number} in {subject_name}")
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to update answers in the database
db_path = "past_papers.db"  # Replace with the actual path to your database file
update_answer_in_db(db_path)
