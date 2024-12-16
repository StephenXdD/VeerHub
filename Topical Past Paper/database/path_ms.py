import sqlite3  # Import sqlite3 library for database operations

def generate_file_path(variant, year, subject_code, paper_variant, question_number):
    """
    Generate a file path based on session, year, subject, paper type, and question number.
    Ensures the path uses forward slashes and replaces '/' in the variant with '_'.
    """
    # Replace forward slash with underscore in the variant
    variant = variant.replace("/", "_")
    
    # Always set paper number to 1 (fixed)
    paper_number = 1  # Always set paper number to 1 for the file path
    
    # Generate file path using the paper number (always 1) and dynamic question number from the database
    file_path = f"C:/Users/Projects/TPP/output_questions/ms/{subject_code}/{year}/{variant}/{paper_variant}/{question_number}.pdf"
    
    # Ensure the use of forward slashes
    return file_path.replace("\\", "/")

def get_paper_data_from_db():
    conn = sqlite3.connect("past_papers.db")
    cursor = conn.cursor()

    # SQL query to fetch paper data for 'Physics' and paper_number = 1
    cursor.execute("SELECT ROWID, variant, year, subject_code, paper_variant, question_number FROM past_papers WHERE Subject_name = 'Pure Math' AND paper_number = 1")
    
    papers = cursor.fetchall()
    conn.close()

    return papers

def update_answer_column(paper_id, file_path):
    """
    Update the 'answer' column in the database with the generated file path for the paper.
    """
    try:
        conn = sqlite3.connect("past_papers.db")  # Connect to the database
        cursor = conn.cursor()

        # SQL query to update the answer column with the generated file path
        cursor.execute("UPDATE past_papers SET answer = ? WHERE ROWID = ?", (file_path, paper_id))

        conn.commit()  # Commit the changes to the database
        conn.close()  # Close the connection
        print(f"Updated paper with ID {paper_id} to path: {file_path}")

    except sqlite3.OperationalError as e:
        print(f"Error updating the database: {e}")
        print("The database might be in read-only mode, check file permissions.")

def generate_paths():
    papers = get_paper_data_from_db()
    
    # Generate file paths for each paper entry and update the answer column
    for paper in papers:
        paper_id, variant, year, subject_code, paper_variant, question_number = paper
        
        # Generate the file path dynamically using the fetched question_number
        file_path = generate_file_path(variant, year, subject_code, paper_variant, question_number)
        
        # Update the answer column with the generated file path
        update_answer_column(paper_id, file_path)

        print(f"Updated paper with file path: {file_path}")

# Example of calling the function to generate paths and update the database
generate_paths()
