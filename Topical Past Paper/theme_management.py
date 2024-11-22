import streamlit as st

# Path to the Streamlit configuration file
config_file_path = "C:\\Users\\Dev Joshi\\.streamlit\\config.toml"

# Light theme revised for better contrast and readability
light_theme = """
[theme]
primaryColor = "#D3B9D4"  # A softer lavender for primary actions
backgroundColor = "#FFFFFF"  # White background for maximum contrast
secondaryBackgroundColor = "#F2EAFB"  # Very light lavender for secondary surfaces
textColor = "#333333"  # Dark gray text for enhanced readability
font = "Inter"  # Updated to use Inter font
"""

# Dark theme with white text
dark_theme = """
[theme]
primaryColor = "#D3B9D4"  # Soft purple for primary actions
backgroundColor = "#73648A"  # Pure black for the background
secondaryBackgroundColor = "#000000"  # Muted purple for surfaces
textColor = "#FFFFFF"  # White for all text
font = "Inter"  # Updated to use Inter font
"""

def write_theme_to_config(theme):
    """
    Writes the selected theme configuration to the config.toml file.
    """
    try:
        with open(config_file_path, "w") as config_file:
            config_file.write(theme)
    except Exception as e:
        st.error(f"Failed to update theme: {e}")

def toggle_theme():
    """
    Toggles between light and dark mode without rerunning the app.
    """
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = False  # Default to light mode

    if st.session_state.dark_mode:
        button_text = "Switch to Light Mode"
        current_theme = light_theme
    else:
        button_text = "Switch to Dark Mode"
        current_theme = dark_theme

    if st.button(button_text, key="toggle_theme_button"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        write_theme_to_config(current_theme)
