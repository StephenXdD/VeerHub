import streamlit as st

def main():
    # Title for the About Us Page
    st.title("About Us")

    # Introduction text or tagline
    st.write("Meet the minds behind our innovative platform.")

    # Create columns for the team members
    col1, col2 = st.columns(2)

    # Information about Veer Sanghvi
    with col1:
        st.header("Veer Sanghvi")
        st.image("1280x720.png", width=300)  # Ensure the path to Veer's image is correct
        st.subheader("Role: Co-Founder & Frontend Lead")
        st.write("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """)

    # Information about Dev Joshi
    with col2:
        st.header("Dev Joshi")
        st.image("1280x720.png", width=300)  # Ensure the path to Dev's image is correct
        st.subheader("Role: Co-Founder & Backend Lead")
        st.write("""
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        """)

    # Footer or additional information
    st.markdown("---")
    st.subheader("Our Mission")
    st.write("We strive to deliver impactful, insightful, and innovative content to our users, empowering them to make informed decisions.")

if __name__ == "_main_":
    main()