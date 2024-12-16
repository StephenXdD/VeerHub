import streamlit as st
from app import main as run_app_logic  # Import the main app logic from app.py
from aboutus import main as run_about_us  # Import the About Us page logic from aboutus.py
from worksheet import main as run_worksheet  # Import the Worksheet page logic from worksheet.py
from quiz import main as run_quiz  # Import the Quiz page logic from quiz.py

def set_theme():
    st.set_page_config(page_title="Past Paper Filter Tool", page_icon="📚", layout="wide")

def switch_page(page_name):
    st.session_state["current_page"] = page_name
    st.rerun()

# Initialize the theme and page setup
set_theme()

# Enhanced CSS styling with transparent background
st.markdown("""
    <style>
    body, html, header, .stApp {
        background-color: rgba(240, 244, 248, 0.8); /* Light soft background with transparency */
        color: #2D2D2D; /* Dark text for better readability */
        font-family: 'Inter', sans-serif;
    }

    .main-content {
        margin-top: 80px;
        text-align: center;
    }

    h1 {
        font-size: 3.5rem;
        color: #1F2937; /* Deep grayish-blue for the main heading */
        text-shadow: 1px 1px 4px rgba(150, 150, 150, 0.7);
        margin-bottom: 15px;
    }

    h2 {
        font-size: 1.3rem;
        color: #4B5563; /* Softer gray for secondary text */
        text-shadow: 1px 1px 3px rgba(150, 150, 150, 0.6);
        margin-bottom: 15px;
        text-align: center;               
    }

    .footer {
        background-color: rgba(74, 88, 153, 0.9); /* A rich dark blue with transparency */
        color: #F4F7F5; /* Light off-white text */
        text-align: center;
        padding: 15px;
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
    }

    .footer a {
        color: #F4F7F5;
        text-decoration: none;
        margin: 0 10px;
    }

    .footer a:hover {
        color: #E0FFFF; /* Light cyan color on hover */
    }

    .footer p {
        font-size: 0.9rem;
    }

    /* Button styling */
    .stButton>button {
        background-color: rgba(74, 88, 153, 0.9); /* Deep blue button background with transparency */
        border: none;
        color: #FFFFFF; /* White text */
        border-radius: 10px;
        font-size: 18px;
        padding: 12px 25px;
        transition: all 0.3s ease, transform 0.2s ease, box-shadow 0.2s ease;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        display: block;
        margin: 10px auto;
        width: 60%;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, rgba(167, 162, 169, 0.8), rgba(74, 88, 153, 0.9));
        color: #F4F7F5;
        transform: translateY(-3px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.3);
        cursor: pointer;
        border-radius: 100px;
    }

    .stButton>button:active {
        transform: translateY(1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
        background: linear-gradient(135deg, rgba(167, 162, 169, 0.8), rgba(74, 88, 153, 0.9))
    }
    
    /* Improved hover and interaction styles */
    .stButton>button:focus {
        outline: none;
        box-shadow: 0 0 0 2px rgba(167, 162, 169, 0.8); /* Subtle outline on focus for better accessibility */
        background: linear-gradient(135deg, rgba(167, 162, 169, 0.8), rgba(74, 88, 153, 0.9))x
    }

    </style>
""", unsafe_allow_html=True)

# Parse query parameters and initialize session state for navigation
if "current_page" not in st.session_state:
    st.session_state.current_page = "home"

# Define the routing logic based on current page
if st.session_state.current_page == "home":
    # Main Title and Content
    st.markdown("<div class='main-content'><h1>Welcome to the Past Paper Filter Tool</h1>", unsafe_allow_html=True)
    st.markdown("<h2>Easily filter and explore past papers by selecting specific subjects, topics, and other criteria.</h2>", unsafe_allow_html=True)

    # Centered buttons
    with st.container():
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
        with col2:
            if st.button("Past Paper Filtering Tool", key='filter_btn'):
                switch_page("app")
            if st.button("Worksheet Builder", key='worksheet_btn'):
                switch_page("worksheet")
            if st.button("Quiz", key="quiz_btn"):
                switch_page("quiz")
            if st.button("About Us", key='about_us_btn'):
                switch_page("aboutus")
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>&copy; 2024 Past Paper Filter Tool | <a href="#">Privacy Policy</a> | <a href="#">Terms of Service</a></p>
            <p>Follow us: 
                <a href="#">Facebook</a> | 
                <a href="#">Twitter</a> | 
                <a href="#">Instagram</a>
            </p>
        </div>
    """, unsafe_allow_html=True)

elif st.session_state.current_page == "app":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("🏠 Back to Home"):
            # Clear session state and reload the page
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    run_app_logic()

elif st.session_state.current_page == "aboutus":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("🏠 Back to Home"):
            # Clear session state and reload the page
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    run_about_us()

elif st.session_state.current_page == "worksheet":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("🏠 Back to Home"):
            # Clear session state and reload the page
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    run_worksheet()

elif st.session_state.current_page == "quiz":
    with st.sidebar:
        st.header("📍 Navigation")
        if st.button("🏠 Back to Home"):
            # Clear session state and reload the page
            for key in st.session_state.keys():
                del st.session_state[key]
            st.rerun()
    run_quiz()