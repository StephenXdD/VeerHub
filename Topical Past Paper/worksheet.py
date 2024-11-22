import streamlit as st
import random
from PyPDF2 import PdfMerger
import os
from filter_logic import (
    connect_to_db, 
    get_subjects, 
    get_topics, 
    get_subtopics, 
    get_years, 
    get_variants, 
    get_paper_numbers, 
    get_paper_variants, 
    get_difficulties,
    filter_papers
)

# Add CSS file to Streamlit app
def load_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def handle_filters_and_generate(conn, selected_subject, selected_years, selected_variants, selected_difficulties, selected_topics, selected_subtopics, selected_paper_numbers, selected_paper_variants):
    """Handles filtering and generating an array of paper paths (for both questions and answers)."""
    # Filter the papers based on selected criteria
    filtered_data = filter_papers(
        conn,
        selected_subject,
        selected_years,
        selected_variants,
        selected_difficulties,
        selected_topics,
        selected_subtopics,
        selected_paper_numbers,
        selected_paper_variants
    )
    
    # Collect the paper paths in an array for both questions and answers
    question_paths = []
    answer_paths = []
    
    if filtered_data:
        st.success(f"Found {len(filtered_data)} papers matching your criteria.")
        
        for paper in filtered_data:
            question_path = paper[11]  # assuming the 12th column is the question file path
            answer_path = paper[12]    # assuming the 13th column is the answer file path
            
            # Add paths to their respective lists
            question_paths.append(question_path)
            answer_paths.append(answer_path)
    
    else:
        st.warning("No papers found with the selected filters.")
    
    # Randomize both question and answer paths while keeping them in sync
    combined_paths = list(zip(question_paths, answer_paths))  # Pair up question and answer paths
    random.shuffle(combined_paths)  # Shuffle the pairs
    
    # Separate the shuffled question and answer paths back into their own lists
    question_paths, answer_paths = zip(*combined_paths)  # Unzip into two lists
    
    return list(question_paths), list(answer_paths)

def merge_pdfs(question_paths, answer_paths, output_question_path="merged_question_paper.pdf", output_answer_path="merged_answer_sheet.pdf"):
    """Merges a list of PDFs into two PDFs: one for questions and one for answers."""
    question_merger = PdfMerger()
    answer_merger = PdfMerger()
    
    # Append each question PDF and answer PDF to their respective mergers
    for question_path, answer_path in zip(question_paths, answer_paths):
        if os.path.exists(question_path):
            question_merger.append(question_path)  # Append the question PDF
        else:
            st.warning(f"Question file not found: {question_path}")
        
        if os.path.exists(answer_path):
            answer_merger.append(answer_path)  # Append the answer PDF
        else:
            st.warning(f"Answer file not found: {answer_path}")
    
    # Output merged question PDF
    try:
        question_merger.write(output_question_path)
        question_merger.close()
    except Exception as e:
        st.error(f"Error while merging question papers: {e}")

    # Output merged answer PDF
    try:
        answer_merger.write(output_answer_path)
        answer_merger.close()
    except Exception as e:
        st.error(f"Error while merging answer sheets: {e}")

def main():
    # Load the CSS styles
    load_css()

    # Establish a connection to the database
    with connect_to_db() as conn:
        # Fetch all distinct options for filters from the database
        subjects = get_subjects(conn)

        # Sidebar for filters
        st.sidebar.header("Filter Options")
        
        # Subject filter
        selected_subject = st.sidebar.selectbox("Select Subject", subjects)
        
        # Dynamically fetch topics based on the selected subject
        topics = get_topics(conn, selected_subject)
        selected_topics = st.sidebar.multiselect("Select Topics", topics)
        
        # Dynamically fetch subtopics based on the selected subject and topics
        subtopics = get_subtopics(conn, selected_subject, selected_topics)
        selected_subtopics = st.sidebar.multiselect("Select Subtopics", subtopics)
        
        # Dynamically fetch years based on the selected subject, topics, and subtopics
        years = get_years(conn, selected_subject, selected_topics, selected_subtopics)
        selected_years = st.sidebar.multiselect("Select Years", years)
        
        # Dynamically fetch variants based on selected criteria
        variants = get_variants(conn, selected_subject, selected_years, selected_topics, selected_subtopics)
        selected_variants = st.sidebar.multiselect("Select Variants", variants)
        
        # Dynamically fetch paper numbers based on selected criteria
        paper_numbers = get_paper_numbers(conn, selected_subject, selected_years, selected_variants, selected_topics, selected_subtopics)
        selected_paper_numbers = st.sidebar.multiselect("Select Paper Numbers", paper_numbers)
        
        # Dynamically fetch paper variants based on selected criteria
        paper_variants = get_paper_variants(conn, selected_subject, selected_years, selected_variants, selected_paper_numbers, selected_topics, selected_subtopics)
        selected_paper_variants = st.sidebar.multiselect("Select Paper Variants", paper_variants)
        
        # Dynamically fetch difficulties based on all selected criteria
        difficulties = get_difficulties(conn, selected_subject, selected_years, selected_variants, selected_paper_numbers, selected_paper_variants, selected_topics, selected_subtopics)
        selected_difficulties = st.sidebar.multiselect("Select Difficulty", difficulties)

        # When the user clicks the button, call the function to filter papers and display results
        if st.sidebar.button("Generate Papers"):
            with st.spinner("Filtering papers..."):
                question_paths, answer_paths = handle_filters_and_generate(
                    conn,
                    selected_subject,
                    selected_years,
                    selected_variants,
                    selected_difficulties,
                    selected_topics,
                    selected_subtopics,
                    selected_paper_numbers,
                    selected_paper_variants
                )

                # Merge the PDFs from the randomized paths
                if question_paths and answer_paths:
                    # Merge the PDFs (question + answer)
                    output_question_path = "merged_question_paper.pdf"
                    output_answer_path = "merged_answer_sheet.pdf"
                    merge_pdfs(question_paths, answer_paths, output_question_path, output_answer_path)

                    # When both PDFs have been merged, show the download buttons for the separate files
                    if os.path.exists(output_question_path) and os.path.exists(output_answer_path):
                        # Open the files directly and prepare for download
                        with open(output_question_path, "rb") as f:
                            question_file_data = f.read()

                        with open(output_answer_path, "rb") as f:
                            answer_file_data = f.read()

                        # Provide separate download buttons without causing page refresh
                        st.download_button(
                            label="Download Merged Question Paper",
                            data=question_file_data,
                            file_name="merged_question_paper.pdf",
                            mime="application/pdf"
                        )

                        st.download_button(
                            label="Download Merged Answer Sheet",
                            data=answer_file_data,
                            file_name="merged_answer_sheet.pdf",
                            mime="application/pdf"
                        )

                    else:
                        st.warning("Something went wrong. Please try again.")

                else:
                    st.warning("No papers found to merge.")

if __name__ == "__main__":
    main()