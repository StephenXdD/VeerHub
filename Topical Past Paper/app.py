import streamlit as st
from filter_logic import (
    connect_to_db, get_subjects, get_topics, get_subtopics,
    get_years, get_variants, get_paper_numbers, get_paper_variants,
    get_difficulties, filter_papers
)
from pdf_utils import display_pdfs, download_pdf, merge_pdfs, create_zip
from doubly_linked_list import DoublyLinkedList
from theme_management import toggle_theme  # Import your theme toggle function
import random
import os
import zipfile
from io import BytesIO
import time  # Import time to use sleep for simulating progress

def load_css():
    with open("styles.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
def main():
    with st.sidebar:
        st.header("🌙 Theme Toggle")
        toggle_theme()  # Add theme toggle button from your theme_management.py
    load_css()

    # Main app title and description
    st.title("📚 Past Paper Filter Tool")
    st.write("Easily filter past papers by selecting specific subjects, topics, and other criteria.")

    # Establish database connection using context manager
    with connect_to_db() as conn:
        # Sidebar for filters with collapsible sections
        with st.sidebar:
            st.header("📝 Filter Options")

            # Clear Selections Button clears everything that is being displayed and resets the filters
            if st.button("Reset Filters", key="reset_filters"):
                keys_to_reset = [
                    'topics_multiselect', 'subtopics_multiselect', 'years_multiselect',
                    'variants_multiselect', 'paper_numbers_multiselect', 'paper_variants_multiselect',
                    'difficulties_multiselect', 'question_paths_list', 'answer_paths_list',
                    'current_index', 'show_question'
                ]
                for key in keys_to_reset:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()  # Refresh the page to update UI and display new filter results

            # Get subjects with help text
            subject_list = get_subjects(conn)
            selected_subject = st.selectbox(
                "Subject:",
                subject_list,
                key="subject_select",
                help="Select the subject to filter past papers."
            )

            # Initialize selections
            selected_topics = st.session_state.get("topics_multiselect", [])
            selected_subtopics = st.session_state.get("subtopics_multiselect", [])
            selected_years = st.session_state.get("years_multiselect", [])
            selected_variants = st.session_state.get("variants_multiselect", [])
            selected_paper_numbers = st.session_state.get("paper_numbers_multiselect", [])
            selected_paper_variants = st.session_state.get("paper_variants_multiselect", [])
            selected_difficulties = st.session_state.get("difficulties_multiselect", [])

            if selected_subject:
                with st.expander("Select Topics and Subtopics"):
                    topics = get_topics(conn, selected_subject)
                    select_all_topics = st.checkbox("Select All Topics", key="all_topics")
                    selected_topics = st.multiselect(
                        "Topics:",
                        topics,
                        default=topics if select_all_topics else [],
                        key="topics_multiselect",
                        help="Choose one or more topics to narrow down the papers."
                    )

                    if selected_topics:
                        subtopics = get_subtopics(conn, selected_subject, selected_topics)
                        select_all_subtopics = st.checkbox("Select All Subtopics", key="all_subtopics")
                        selected_subtopics = st.multiselect(
                            "Subtopics:",
                            subtopics,
                            default=subtopics if select_all_subtopics else [],
                            key="subtopics_multiselect",
                            help="Choose subtopics for more specific filtering."
                        )

                with st.expander("Select Year and Variants"):
                    years = get_years(conn, selected_subject, selected_topics, selected_subtopics)
                    select_all_years = st.checkbox("Select All Years", key="all_years")
                    selected_years = st.multiselect(
                        "Years:",
                        years,
                        default=years if select_all_years else [],
                        key="years_multiselect",
                        help="Select the years for which you want to see past papers."
                    )

                    if selected_years:
                        variants = get_variants(conn, selected_subject, selected_years, selected_topics, selected_subtopics)
                        select_all_variants = st.checkbox("Select All Variants", key="all_variants")
                        selected_variants = st.multiselect(
                            "Variants:",
                            variants,
                            default=variants if select_all_variants else [],
                            key="variants_multiselect",
                            help="Choose paper variants if applicable."
                        )

                with st.expander("Select Paper Numbers and Variants"):
                    if selected_variants:
                        paper_numbers = get_paper_numbers(
                            conn, selected_subject, selected_years,
                            selected_variants, selected_topics, selected_subtopics
                        )
                        select_all_paper_numbers = st.checkbox("Select All Paper Numbers", key="all_paper_numbers")
                        selected_paper_numbers = st.multiselect(
                            "Paper Numbers:",
                            paper_numbers,
                            default=paper_numbers if select_all_paper_numbers else [],
                            key="paper_numbers_multiselect",
                            help="Select specific paper numbers."
                        )

                        if selected_paper_numbers:
                            paper_variants = get_paper_variants(
                                conn, selected_subject, selected_years,
                                selected_variants, selected_paper_numbers,
                                selected_topics, selected_subtopics
                            )
                            select_all_paper_variants = st.checkbox("Select All Paper Variants", key="all_paper_variants")
                            selected_paper_variants = st.multiselect(
                                "Paper Variants:",
                                paper_variants,
                                default=paper_variants if select_all_paper_variants else [],
                                key="paper_variants_multiselect",
                                help="Choose paper variants if available."
                            )

                with st.expander("Select Difficulty Levels"):
                    if selected_paper_variants:
                        difficulties = get_difficulties(
                            conn, selected_subject, selected_years,
                            selected_variants, selected_paper_numbers,
                            selected_paper_variants, selected_topics, selected_subtopics
                        )
                        select_all_difficulties = st.checkbox("Select All Difficulties", key="all_difficulties")
                        selected_difficulties = st.multiselect(
                            "Difficulty Levels:",
                            difficulties,
                            default=difficulties if select_all_difficulties else [],
                            key="difficulties_multiselect",
                            help="Filter papers by difficulty level."
                        )

        # Main area to display filtered results
        st.subheader("🔍 Filtered Results")

        if st.button("Generate Papers", key="generate_papers_button"):
            progress_bar = st.progress(0)  # Initialize progress bar

            # Use a spinner only for filtering the papers (before the filtering is done)
            with st.spinner("Loading papers..."):
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

            # If papers are found, continue processing and update progress bar
            if filtered_data:
                st.success(f"Found {len(filtered_data)} papers matching your criteria.")
                
                # Separate lists for questions and answers
                question_paths_list = []
                answer_paths_list = []

                for i, paper in enumerate(filtered_data):
                    question_path = paper[11]  # Assuming question PDF path is at index 11
                    answer_path = paper[12]   # Assuming answer PDF path is at index 12
                    question_paths_list.append(question_path)
                    answer_paths_list.append(answer_path)

                    # Update progress bar manually with small increments
                    progress = (i + 1) / len(filtered_data) * 100
                    progress_bar.progress(int(progress))  # Update the progress bar
                    time.sleep(0.0005)  # Simulate some delay

                # Shuffle both lists in parallel to maintain the pairing
                combined = list(zip(question_paths_list, answer_paths_list))
                random.shuffle(combined)
                question_paths_list, answer_paths_list = zip(*combined)

                # Store the shuffled lists in session state
                st.session_state.question_paths_list = list(question_paths_list)
                st.session_state.answer_paths_list = list(answer_paths_list)
                st.session_state.current_index = 0  # Start at the first question-answer pair
                st.session_state.show_question = True  # Initially show the question only
        if "question_paths_list" in st.session_state and st.session_state.question_paths_list:
            current_index = st.session_state.current_index
            question_pdf_path = st.session_state.question_paths_list[current_index]
            answer_pdf_path = st.session_state.answer_paths_list[current_index]

            # Display the "Show Answer" button and toggle between question and answer
            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                if st.button("Show Answer" if st.session_state.show_question else "Show Question", key="show_answer_button"):
                    st.session_state.show_question = not st.session_state.show_question
                    st.rerun()

            # Display the appropriate PDF based on whether the question or answer should be visible
            display_pdfs(question_pdf_path, answer_pdf_path, show_question=st.session_state.show_question)

            # Navigation buttons (Next and Previous)
            col1, col2, col3 = st.columns([1, 3, 1])
            with col1:
                if st.button("Previous", key="previous_button") and current_index > 0:
                    st.session_state.current_index -= 1
                    st.rerun()

            with col3:
                if st.button("Next", key="next_button") and current_index < len(st.session_state.question_paths_list) - 1:
                    st.session_state.current_index += 1
                    st.rerun()


if __name__ == "__main__":
    main()