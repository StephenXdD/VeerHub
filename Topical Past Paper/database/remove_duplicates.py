import sqlite3
import pandas as pd

# Path to your .db file
db_path = "past_papers.db"  # Replace with your actual .db file path

# Connect to the SQLite database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Specify the table name in your database
table_name = "past_papers"  # Replace with the actual table name

# Load the data into a pandas DataFrame
query = f"SELECT * FROM {table_name}"
df = pd.read_sql_query(query, conn)

# Check for duplicate rows (all columns must match)
duplicates = df[df.duplicated(keep=False)]

if duplicates.empty:
    print("No duplicate rows found.")
else:
    print(f"{len(duplicates)} duplicate rows found and will be removed.")
    
    # Save duplicates to a separate file for review
    duplicates.to_csv("duplicate_rows.csv", index=False)
    print("Duplicate rows saved to 'duplicate_rows.csv' for inspection.")
    
    # Remove duplicates
    cleaned_df = df.drop_duplicates()

    # Replace the table with the cleaned data
    cleaned_df.to_sql(table_name, conn, if_exists="replace", index=False)
    print(f"Duplicates removed. Cleaned data saved back to the '{table_name}' table.")

# Close the connection
conn.close()
