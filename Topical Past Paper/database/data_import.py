import sqlite3
import pandas as pd

def create_connection(db_file):
    """Create a database connection to the SQLite database specified by db_file."""
    conn = sqlite3.connect(db_file)
    return conn

def remove_not_null_constraint(conn):
    """Remove the NOT NULL constraint from the Topic column."""
    # Creating a new table without the NOT NULL constraint on Topic column
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS past_papers_new (
        Subject_name TEXT,
        Subject_code TEXT,
        Topic TEXT,
        Sub_topic TEXT,
        Paper_number INTEGER,
        Paper_variant TEXT,
        Variant TEXT,
        Difficulty TEXT,
        Year INTEGER,
        Marks INTEGER,
        Question_Number INTEGER,
        Question TEXT,
        Answer TEXT
    );
    """

    # Execute the SQL to create a new table
    conn.execute(create_table_sql)

    # Copy data from old table to new table (ignore the constraint)
    insert_sql = """
    INSERT INTO past_papers_new (
        Subject_name, Subject_code, Topic, Sub_topic, Paper_number, Paper_variant, 
        Variant, Difficulty, Year, Marks, Question_Number, Question, Answer
    )
    SELECT 
        Subject_name, Subject_code, Topic, Sub_topic, Paper_number, Paper_variant, 
        Variant, Difficulty, Year, Marks, Question_Number, Question, Answer
    FROM past_papers;
    """
    conn.execute(insert_sql)

    # Drop the old table
    conn.execute("DROP TABLE past_papers;")

    # Rename the new table to the original table name
    conn.execute("ALTER TABLE past_papers_new RENAME TO past_papers;")

    # Commit the changes
    conn.commit()
    print("NOT NULL constraint removed from 'Topic' column.")

def insert_data_from_excel(conn, excel_file):
    """Insert data from an Excel file into the past_papers table."""
    # Load the Excel file into a DataFrame
    df = pd.read_excel(excel_file)
    
    # Check for missing values in the Topic column and handle them
    if df['Topic'].isnull().any():
        print("Warning: Missing 'Topic' values found. Replacing with 'Unknown'.")
        df['Topic'].fillna('Unknown', inplace=True)  # Replace missing values with 'Unknown'
    
    # Rename columns in DataFrame to match the database table exactly
    df.columns = [
        "Subject_name", "Subject_code", "Topic", "Sub_topic", "Paper_number", 
        "Paper_variant", "Variant", "Difficulty", "Year", "Marks", "Question_Number"
    ]

    # Prepare the SQL insertion command
    insert_sql = """
    INSERT INTO past_papers (
        Subject_name, Subject_code, Topic, Sub_topic, Paper_number, Paper_variant, 
        Variant, Difficulty, Year, Marks, Question_Number
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    # Insert each row of data
    for row in df.itertuples(index=False):
        conn.execute(insert_sql, row)

    # Commit changes
    conn.commit()
    print("Data inserted successfully from Excel file.")

def main():
    # Specify the database and Excel file names
    database = 'past_papers.db'
    excel_file = 'STATS.xlsx'  # File is in the same folder
    
    # Create a database connection
    conn = create_connection(database)

    # Remove the NOT NULL constraint from the Topic column (if it exists)
    remove_not_null_constraint(conn)

    # Insert data from Excel into the past_papers table
    insert_data_from_excel(conn, excel_file)
    
    # Close the database connection
    conn.close()

if __name__ == "__main__":
    main()
