import sqlite3

def clear_answers_in_db(db_path, subject_name="Physics"):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Update the 'Answer' column to NULL (or empty string) for all rows where the subject is Physics
    cursor.execute("""
        UPDATE past_papers
        SET Answer = ''
        WHERE subject_name = ?
    """, (subject_name,))
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()

# Call the function to clear answers in the database
db_path = "past_papers.db"  # Replace with the actual path to your database file
clear_answers_in_db(db_path)
