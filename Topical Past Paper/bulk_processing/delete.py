import sqlite3

def clear_question_column():
    """
    Clear the contents of the 'question' column where the subject_name is 'Accounting'.
    """
    conn = sqlite3.connect("past_papers.db")
    cursor = conn.cursor()

    # SQL query to update the question column to NULL where subject_name is 'Accounting'
    cursor.execute("UPDATE past_papers SET question = NULL WHERE Subject_name = 'Accounting'")
    
    conn.commit()
    conn.close()

    print("Cleared the 'question' column for all Accounting papers.")

# Example of calling the function to clear the question column
clear_question_column()
