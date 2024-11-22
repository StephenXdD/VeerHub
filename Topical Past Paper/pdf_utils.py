import streamlit as st
import os
from pdf2image import convert_from_path

def convert_pdf_to_images(pdf_path):
    """
    Convert a PDF file to a list of images, one per page.
    :param pdf_path: Path to the PDF file
    :return: List of PIL Image objects
    """
    try:
        images = convert_from_path(pdf_path, 200)  # DPI can be adjusted for higher quality
        return images
    except Exception as e:
        st.error(f"An error occurred while converting the PDF: {e}")
        return []

def display_pdf(pdf_path):
    """
    Display the pages of a PDF side by side without fullscreen buttons.
    :param pdf_path: Path to the PDF file
    """
    images = convert_pdf_to_images(pdf_path)
    if not images:
        st.error("No images to display. The PDF might be empty or invalid.")
        return

    cols = st.columns(len(images))  # Create a column for each page
    for i, image in enumerate(images):
        with cols[i]:
            st.image(image, caption=f"Page {i + 1}", use_column_width=True)

def download_pdf(file_path):
    """
    Function to allow downloading of the PDF file.
    """
    if not file_path:
        st.error("File path is None or empty!")
        return

    if not os.path.exists(file_path):
        st.error(f"PDF file not found at the path: {file_path}")
        return

    with open(file_path, "rb") as file:
        binary_data = file.read()
        st.download_button(
            label="📥 Download PDF",
            data=binary_data,
            file_name=os.path.basename(file_path),
            mime="application/pdf",
            key=f"download_pdf_button_{file_path}"
        )
