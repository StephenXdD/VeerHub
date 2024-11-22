import streamlit as st
from app import main as run_app_logic  # Import the main app logic from app.py
from aboutus import main as run_about_us  # Import the About Us page logic from aboutus.py
from worksheet import main as run_worksheet  # Import the Worksheet page logic from worksheet.py
from quiz import main as run_quiz  # Import the Quiz page logic from quiz.py

def set_theme():
    # Theme settings with custom colors
    st.set_page_config(page_title="Past Paper Filter Tool", page_icon="📚", layout="wide")

def switch_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

# Initialize the theme and page setup
set_theme()

# Parse query parameters and initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Define the routing logic based on current page
if st.session_state.current_page == "home":
    # Enhanced CSS for better visuals
    st.markdown("""
        <style>
        /* Ensure all parts of the app including headers and footers are covered */
        body, html, header, .stApp, .stHeader, .stFooter {
            background: linear-gradient(135deg, #3498db, #2c3e50) !important;
            color: #ffffff !important;
            font-family: "Arial", sans-serif;
        }
        /* Styling for titles and text */
        h1 {
            font-size: 3rem;
            color: #ffffff;
            text-align: center;
            margin-bottom: 20px;
        }
        p {
            text-align: center;
            font-size: 1.2rem;
            color: #dcdcdc;
            margin-bottom: 30px;
        }
        /* Styling for buttons */
        .stButton>button {
            border-radius: 25px;
            border: 2px solid #ffffff;
            color: #ffffff;
            background-color: rgba(255, 255, 255, 0.1);
            font-size: 32px;
            padding: 15px 40px;
            margin: 0 auto;
            display: block;
            transition: background-color 0.3s, border-color 0.3s, color 0.3s, transform 0.2s;
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.2);
            height: 100px;
            width: 80%;  /* Adjusted width for better center alignment */
        }
        .stButton>button:hover {
            background-color: rgba(255, 255, 255, 0.1);
            color: #000000; /* Change text color to black on hover */
            border-color: #00FFFF; /* Change outline to cyan on hover */
            transform: translateY(-3px);
        }
        </style>
        """, unsafe_allow_html=True)

    # Main Title
    st.markdown("<h1>Welcome to the Past Paper Filter Tool</h1>", unsafe_allow_html=True)
    st.markdown("<p>Easily filter and explore past papers by selecting specific subjects, topics, and other criteria.</p>", unsafe_allow_html=True)

    # Centered button layout
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col2:
            if st.button("Past Paper Filtering Tool", key='filter_btn'):
                switch_page("app")
            # Add button to navigate to the worksheet page below the past paper filtering tool button
            if st.button("Worksheet Builder", key='worksheet_btn'):
                switch_page("worksheet")
            if st.button("Quiz", key="quiz_btn"):
                switch_page("quiz")
            if st.button("About Us", key='about_us_btn'):
                switch_page("aboutus")
            

elif st.session_state.current_page == "app":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("Back to Home"):
            switch_page("home")
    run_app_logic()

elif st.session_state.current_page == "aboutus":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("Back to Home"):
            switch_page("home")
    run_about_us()

elif st.session_state.current_page == "worksheet":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("Back to Home"):
            switch_page("home")
    run_worksheet()  # Call the logic for the worksheet page

elif st.session_state.current_page == "quiz":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("Back to Home"):
            switch_page("home")
    run_quiz()