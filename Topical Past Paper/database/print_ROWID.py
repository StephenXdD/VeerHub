import sqlite3

def find_rowid_for_answer(file_path):
    # Connect to the database (replace 'your_database.db' with the actual database name)
    conn = sqlite3.connect('past_papers.db')  # Adjust the database path if needed
    cursor = conn.cursor()

    # SQL query to find the ROWID where the Answer column contains the file path
    query = "SELECT ROWID FROM past_papers WHERE Answer = ?"

    # Execute the query with the file path as parameter
    cursor.execute(query, (file_path,))
    
    # Fetch all results
    rows = cursor.fetchall()

    if rows:
        # Display the ROWID(s) where the Answer column contains the file path
        for row in rows:
            print(f"ROWID: {row[0]}")  # row[0] corresponds to the ROWID
    else:
        print("No matching row found.")

    # Close the connection
    conn.close()

# Specify the file path you're searching for
file_path = "C:/Users/Projects/TPP/output_questions/ms/9708/2022/Feb_March/12/8.pdf"

# Call the function to find and display the ROWID(s)
find_rowid_for_answer(file_path)
