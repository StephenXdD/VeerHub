import sqlite3 as s3

def connect_to_db(db_name='past_papers.db'):
    """Establish a connection to the SQLite database."""
    try:
        conn = s3.connect(db_name)
        return conn
    except s3.Error as e:
        raise Exception(f"Database connection error: {e}")

def get_distinct_values(conn, column_name, filters=None):
    """Generic method to get distinct values for a given column with optional filters."""
    base_query = f"SELECT DISTINCT {column_name} FROM past_papers WHERE question IS NOT NULL"
    params = []
    if filters:
        query_parts = []
        for key, value in filters.items():
            if isinstance(value, list):
                # Use IN for lists
                query_parts.append(f"{key} IN ({','.join(['?'] * len(value))})")
                params.extend(value)
            else:
                query_parts.append(f"{key} = ?")
                params.append(value)
        if query_parts:
            base_query += " AND " + " AND ".join(query_parts)
    
    c = conn.cursor()
    c.execute(base_query, tuple(params))
    return [row[0] for row in c.fetchall()]

def get_subjects(conn):
    """Retrieve distinct subjects from the database with valid 'question' values."""
    return get_distinct_values(conn, 'Subject_name')

def get_topics(conn, selected_subject):
    """Fetch topics for the chosen subject with valid 'question' values."""
    return get_distinct_values(conn, 'topic', {'Subject_name': selected_subject})

def get_subtopics(conn, selected_subject, selected_topics):
    """Fetch subtopics based on selected topics, ensuring valid 'question' values."""
    filters = {'Subject_name': selected_subject}
    if selected_topics:
        if isinstance(selected_topics, list):
            # Use IN for multiple topics
            query = "SELECT DISTINCT sub_topic FROM past_papers WHERE Subject_name = ? AND topic IN ({}) AND question IS NOT NULL".format(','.join(['?'] * len(selected_topics)))
            c = conn.cursor()
            c.execute(query, [selected_subject] + selected_topics)  # Pass selected_subject and the list of selected_topics
            return [row[0] for row in c.fetchall()]
        else:
            filters['topic'] = selected_topics
    return get_distinct_values(conn, 'sub_topic', filters)

def get_years(conn, selected_subject, selected_topics, selected_subtopics):
    """Fetch years based on selected topics and subtopics, ensuring valid 'question' values."""
    filters = {'Subject_name': selected_subject}
    if selected_topics:
        filters['topic'] = selected_topics
    if selected_subtopics:
        filters['sub_topic'] = selected_subtopics
    return get_distinct_values(conn, 'Year', filters)

def get_variants(conn, selected_subject, selected_years, selected_topics, selected_subtopics):
    """Fetch variants based on selected years, topics, and subtopics, ensuring valid 'question' values."""
    filters = {'Subject_name': selected_subject, 'Year': selected_years}
    if selected_topics:
        filters['topic'] = selected_topics
    if selected_subtopics:
        filters['sub_topic'] = selected_subtopics
    return get_distinct_values(conn, 'Variant', filters)

def get_paper_numbers(conn, selected_subject, selected_years, selected_variants, selected_topics, selected_subtopics):
    """Fetch paper numbers based on selected years, variants, topics, and subtopics, ensuring valid 'question' values."""
    filters = {'Subject_name': selected_subject, 'Year': selected_years, 'Variant': selected_variants}
    if selected_topics:
        filters['topic'] = selected_topics
    if selected_subtopics:
        filters['sub_topic'] = selected_subtopics
    return get_distinct_values(conn, 'paper_number', filters)

def get_paper_variants(conn, selected_subject, selected_years, selected_variants, selected_paper_numbers, selected_topics, selected_subtopics):
    """Fetch paper variants based on selected years, variants, paper numbers, topics, and subtopics, ensuring valid 'question' values."""
    filters = {'Subject_name': selected_subject, 'Year': selected_years, 'Variant': selected_variants, 'paper_number': selected_paper_numbers}
    if selected_topics:
        filters['topic'] = selected_topics
    if selected_subtopics:
        filters['sub_topic'] = selected_subtopics
    return get_distinct_values(conn, 'paper_variant', filters)

def get_difficulties(conn, selected_subject, selected_years, selected_variants, selected_paper_numbers, selected_paper_variants, selected_topics, selected_subtopics):
    """Fetch difficulties based on all previous selections, ensuring valid 'question' values."""
    filters = {'Subject_name': selected_subject, 'Year': selected_years, 'Variant': selected_variants, 'paper_number': selected_paper_numbers, 'paper_variant': selected_paper_variants}
    if selected_topics:
        filters['topic'] = selected_topics
    if selected_subtopics:
        filters['sub_topic'] = selected_subtopics
    return get_distinct_values(conn, 'Difficulty', filters)

def filter_papers(conn, subject, years, variants, difficulties, topics, subtopics, paper_numbers, paper_variants):
    """Filters the past papers database table based on the selected criteria and valid 'question' values."""
    query_parts = ["Subject_name = ?"]
    params = [subject]

    # Dynamically append filter conditions to the query
    filters = {
        'Year': years,
        'Variant': variants,
        'Difficulty': difficulties,
        'topic': topics,
        'sub_topic': subtopics,
        'paper_number': paper_numbers,
        'paper_variant': paper_variants
    }

    for key, values in filters.items():
        if values:
            # Check if values is a list (i.e., multiple options selected)
            if isinstance(values, list):
                # Use the IN clause for lists
                query_parts.append(f"{key} IN ({','.join(['?'] * len(values))})")
                params.extend(values)
            else:
                # Otherwise, just add a single value
                query_parts.append(f"{key} = ?")
                params.append(values)

    query = f"SELECT * FROM past_papers WHERE " + " AND ".join(query_parts) + " AND question IS NOT NULL"  # Ensure 'question' is not null
    
    c = conn.cursor()
    result = c.execute(query, tuple(params)).fetchall()
    return result

def filter_subjects_by_paper_number_and_answer(conn):
    """Retrieve subjects that have papers with 'Paper_number' = '1' and a single letter answer."""
    query = """
    SELECT DISTINCT Subject_name FROM past_papers
    WHERE Paper_number = '1' AND Answer IN ('A', 'B', 'C', 'D')
    """
    c = conn.cursor()
    c.execute(query)
    return [row[0] for row in c.fetchall()]

