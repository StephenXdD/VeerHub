import sqlite3

# Connect to your database (replace 'your_database.db' with your actual database file)
connection = sqlite3.connect("past_papers.db")
cursor = connection.cursor()

# SQL query to delete the records
delete_query = """
DELETE FROM past_papers
WHERE Variant = 'Oct/Nov' AND Year = 2024;
"""

try:
    # Execute the query
    cursor.execute(delete_query)

    # Commit the changes
    connection.commit()

    print(f"Records deleted successfully.")
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    # Close the connection
    connection.close()
