import sqlite3  # Replace with appropriate library for other databases (e.g., MySQL or psycopg2 for PostgreSQL)

def update_topic(database_path, table_name, old_value, new_value):
    """
    Update the Topic column in a database table, replacing old_value with new_value.

    Args:
        database_path (str): Path to the SQLite database file.
        table_name (str): Name of the table to update.
        old_value (str): The value to replace (e.g., "Accounting concepts").
        new_value (str): The new value to set in place of old_value.
    """
    try:
        # Connect to the database
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        # SQL statement to update the Topic column
        sql_update_query = f"""
            UPDATE {table_name}
            SET Topic = ?
            WHERE Topic = ?;
        """

        # Execute the update query
        cursor.execute(sql_update_query, (new_value, old_value))

        # Commit the changes
        connection.commit()

        # Feedback to the user
        print(f"Updated {cursor.rowcount} rows in the '{table_name}' table.")

    except sqlite3.Error as e:
        print(f"Error occurred: {e}")
    finally:
        # Close the database connection
        if connection:
            connection.close()

# Example usage
database_path = "past_papers.db"  # Path to your SQLite database file
table_name = "past_papers"      # Replace with your table name
old_value = "Work, energy, and power"  # Text to replace
new_value = "Work, energy and power"        # Replacement text

update_topic(database_path, table_name, old_value, new_value)
