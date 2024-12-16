import streamlit as st
import random
from PyPDF2 import PdfMerger
import os
import zipfile
from io import BytesIO
from theme_management import toggle_theme
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
import time  # Import time to use sleep function

# Add CSS file to Streamlit app
def load_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def handle_filters_and_generate(conn, selected_subject, selected_years, selected_variants, selected_difficulties, selected_topics, selected_subtopics, selected_paper_numbers, selected_paper_variants, progress_bar):
    """Handles filtering and generating an array of paper paths (for both questions and answers)."""
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
    
    question_paths = []
    answer_paths = []
    
    if filtered_data:
        st.success(f"Found {len(filtered_data)} papers matching your criteria.")
        
        total_files = len(filtered_data)
        for i, paper in enumerate(filtered_data):
            question_path = paper[11]  # assuming the 12th column is the question file path
            answer_path = paper[12]    # assuming the 13th column is the answer file path
            
            question_paths.append(question_path)
            answer_paths.append(answer_path)

            # Update progress bar manually with small increments
            progress = (i + 1) / total_files * 100  # Get progress as a percentage
            progress = min(max(progress, 0), 100)  # Ensure progress is between 0 and 100
            progress_bar.progress(int(progress))  # Convert progress to integer
            time.sleep(0.0005)  # Increase delay to make the progress slower

    else:
        st.warning("No papers found with the selected filters.")
    
    combined_paths = list(zip(question_paths, answer_paths))
    random.shuffle(combined_paths)
    
    question_paths, answer_paths = zip(*combined_paths)
    
    return list(question_paths), list(answer_paths)

def merge_pdfs(question_paths, answer_paths, output_question_path="merged_question_paper.pdf", output_answer_path="merged_answer_sheet.pdf", progress_bar=None):
    """Merges a list of PDFs into two PDFs: one for questions and one for answers."""
    question_merger = PdfMerger()
    answer_merger = PdfMerger()
    
    total_files = len(question_paths)
    for i, (question_path, answer_path) in enumerate(zip(question_paths, answer_paths)):
        if os.path.exists(question_path):
            question_merger.append(question_path)
        else:
            st.warning(f"Question file not found: {question_path}")
        
        if os.path.exists(answer_path):
            answer_merger.append(answer_path)
        else:
            st.warning(f"Answer file not found: {answer_path}")
        
        # Update progress bar manually with small increments
        progress = (i + 1) / total_files * 100  # Get progress as a percentage
        progress = min(max(progress, 0), 100)  # Ensure progress is between 0 and 100
        if progress_bar:
            progress_bar.progress(int(progress))  # Convert progress to integer
            time.sleep(0.5)  # Increase delay to make the progress slower
    
    try:
        question_merger.write(output_question_path)
        question_merger.close()
    except Exception as e:
        st.error(f"Error while merging question papers: {e}")

    try:
        answer_merger.write(output_answer_path)
        answer_merger.close()
    except Exception as e:
        st.error(f"Error while merging answer sheets: {e}")

def create_zip(question_path, answer_path):
    """Create a ZIP file containing the question and answer PDFs."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        if os.path.exists(question_path):
            zip_file.write(question_path, os.path.basename(question_path))
        if os.path.exists(answer_path):
            zip_file.write(answer_path, os.path.basename(answer_path))
    zip_buffer.seek(0)
    return zip_buffer

def main():
    with st.sidebar:
        st.header("🌙 Theme Toggle")
        toggle_theme()  # Add theme toggle button from your theme_management.py
    load_css()

    with connect_to_db() as conn:
        subjects = get_subjects(conn)
        st.sidebar.header("Filter Options")
        selected_subject = st.sidebar.selectbox("Select Subject", subjects)
        topics = get_topics(conn, selected_subject)
        selected_topics = st.sidebar.multiselect("Select Topics", topics)
        subtopics = get_subtopics(conn, selected_subject, selected_topics)
        selected_subtopics = st.sidebar.multiselect("Select Subtopics", subtopics)
        years = get_years(conn, selected_subject, selected_topics, selected_subtopics)
        selected_years = st.sidebar.multiselect("Select Years", years)
        variants = get_variants(conn, selected_subject, selected_years, selected_topics, selected_subtopics)
        selected_variants = st.sidebar.multiselect("Select Variants", variants)
        paper_numbers = get_paper_numbers(conn, selected_subject, selected_years, selected_variants, selected_topics, selected_subtopics)
        selected_paper_numbers = st.sidebar.multiselect("Select Paper Numbers", paper_numbers)
        paper_variants = get_paper_variants(conn, selected_subject, selected_years, selected_variants, selected_paper_numbers, selected_topics, selected_subtopics)
        selected_paper_variants = st.sidebar.multiselect("Select Paper Variants", paper_variants)
        difficulties = get_difficulties(conn, selected_subject, selected_years, selected_variants, selected_paper_numbers, selected_paper_variants, selected_topics, selected_subtopics)
        selected_difficulties = st.sidebar.multiselect("Select Difficulty", difficulties)

        if st.sidebar.button("Generate Papers"):
            progress_bar = st.progress(0)  # Initialize progress bar
            
            # Filter papers and generate paths
            question_paths, answer_paths = handle_filters_and_generate(
                conn,
                selected_subject,
                selected_years,
                selected_variants,
                selected_difficulties,
                selected_topics,
                selected_subtopics,
                selected_paper_numbers,
                selected_paper_variants,
                progress_bar
            )

            if question_paths and answer_paths:
                output_question_path = "merged_question_paper.pdf"
                output_answer_path = "merged_answer_sheet.pdf"
                
                # Merge PDFs and update progress
                merge_pdfs(question_paths, answer_paths, output_question_path, output_answer_path, progress_bar=progress_bar)

                if os.path.exists(output_question_path) and os.path.exists(output_answer_path):
                    zip_buffer = create_zip(output_question_path, output_answer_path)

                    st.download_button(
                        label="Download All Merged Papers",
                        data=zip_buffer,
                        file_name="merged_papers.zip",
                        mime="application/zip"
                    )
                else:
                    st.warning("Something went wrong. Please try again.")
            else:
                st.warning("No papers found to merge.")

if __name__ == "__main__":
    main()
