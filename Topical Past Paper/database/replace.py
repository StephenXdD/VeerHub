import sqlite3

def update_subject_code():
    # Connect to the database (replace 'past_papers.db' with the actual database name)
    conn = sqlite3.connect('past_papers.db')  # Adjust the database path if needed
    cursor = conn.cursor()

    # SQL query to update the Subject_code where Subject_name is "Pure Math"
    query = "UPDATE past_papers SET Subject_code = ? WHERE Subject_name = ?"

    # Execute the query with the new subject code and the condition
    cursor.execute(query, ("9702", "Physics"))

    # Commit the changes
    conn.commit()

    # Check how many rows were updated
    if cursor.rowcount > 0:
        print(f"Updated {cursor.rowcount} rows where Subject_name is 'Physics'.")
    else:
        print("No rows found with Subject_name 'Physics'.")

    # Close the connection
    conn.close()

# Call the function to update the subject code
update_subject_code()
