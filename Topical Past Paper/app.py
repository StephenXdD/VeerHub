import streamlit as st
import sqlite3
import random
from filter_logic import (
    connect_to_db, get_subjects, get_topics, get_subtopics,
    get_years, get_variants, get_paper_numbers, get_paper_variants,
    get_difficulties, filter_papers
)
from pdf_utils import display_pdf, download_pdf
from doubly_linked_list import DoublyLinkedList
from theme_management import toggle_theme

def load_css(file_name):
    with open(file_name, "r") as file:
        st.markdown(f'<style>{file.read()}</style>', unsafe_allow_html=True)

def main():
    # Sidebar setup for theme toggle
    with st.sidebar:
        st.header("🌙 Theme Toggle")
        toggle_theme()
    load_css("styles.css")  # Load and apply the CSS

    # Main app title and description
    st.title("📚 Past Paper Filter Tool")
    st.write("Easily filter past papers by selecting specific subjects, topics, and other criteria.")

    # Establish database connection using context manager
    with connect_to_db() as conn:
        # Sidebar for filters with collapsible sections
        with st.sidebar:
            st.header("📝 Filter Options")

            # Clear Selections Button
            if st.button("Reset Filters", key="reset_filters"):
                keys_to_reset = [
                    'selected_topics', 'selected_subtopics', 'selected_years', 
                    'selected_variants', 'selected_difficulties', 
                    'paper_paths_list', 'current_node'
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

            if filtered_data:
                st.success(f"Found {len(filtered_data)} papers matching your criteria.")
                
                paper_paths_list = DoublyLinkedList()
                
                for paper in filtered_data:
                    file_path = paper[11]
                    paper_paths_list.append(file_path)
                
                st.session_state.paper_paths_list = paper_paths_list
                all_nodes = paper_paths_list.get_all_nodes()
                if all_nodes:
                    st.session_state.current_node = random.choice(all_nodes)

        if "paper_paths_list" in st.session_state and st.session_state.paper_paths_list:
            if "current_node" not in st.session_state or not st.session_state.current_node:
                st.session_state.current_node = st.session_state.paper_paths_list.head

            if st.session_state.current_node:
                pdf_path = st.session_state.current_node.data
                display_pdf(pdf_path)

                col1, col2, col3 = st.columns([1, 1, 1])
                with col1:
                    if st.button("Previous", key="previous_button"):
                        prev_node = st.session_state.paper_paths_list.get_previous(st.session_state.current_node)
                        if prev_node:
                            st.session_state.current_node = prev_node
                            st.rerun()

                with col3:
                    if st.button("Next", key="next_button"):
                        next_node = st.session_state.paper_paths_list.get_next(st.session_state.current_node)
                        if next_node:
                            st.session_state.current_node = next_node
                            st.rerun()

                with col2:
                    download_pdf(pdf_path)

if __name__ == "__main__":
    main()