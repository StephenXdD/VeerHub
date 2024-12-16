import streamlit as st

# Path to the Streamlit configuration file
config_file_path = "C:\\Users\\Dev Joshi\\.streamlit\\config.toml"

# Updated light theme to match `home.py` light styles
light_theme = """
[theme]
primaryColor = "#FFFFFF"  # Muted blue for primary actions
backgroundColor = "rgb(74, 88, 153)"  # White background for maximum contrast
secondaryBackgroundColor = "#ebebeb"  # Very light gray for secondary surfaces
textColor = "#ebebeb"  # Dark black for enhanced readability
font = "Inter"  # Updated to use Inter font
"""

# Updated dark theme to match `home.py` dark styles
dark_theme = """
[theme]
primaryColor = "#1E2019"  # Muted blue for primary actions
backgroundColor = "rgb(74, 88, 153)"  # Dark black background
secondaryBackgroundColor = "#1a1a1a"  # Dark gray for secondary surfaces
textColor = "#ebebeb"  # White text for contrast on dark mode
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

    # Define current theme and button text based on the mode
    if st.session_state.dark_mode:
        button_text = "Switch to Light Mode"
        current_theme = light_theme
    else:
        button_text = "Switch to Dark Mode"
        current_theme = dark_theme

    # Create a toggle button to switch themes
    if st.button(button_text, key="toggle_theme_button"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        write_theme_to_config(current_theme)
