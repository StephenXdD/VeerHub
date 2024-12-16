import zipfile
import os
import tempfile
from io import BytesIO
from pdf2image import convert_from_path
import streamlit as st
import fitz
from PIL import Image
from PyPDF2 import PdfMerger
import time

def convert_pdf_to_images(pdf_path):
    """
    Convert a PDF to a list of images (one per page).
    """
    try:
        return convert_from_path(pdf_path)
    except Exception as e:
        st.error(f"Error converting PDF to images: {e}")
        return []

def display_pdfs(question_pdf_path, answer_pdf_path, show_question=True):
    """
    Display PDFs for questions or answers based on the show_question flag, supporting enhanced resolution for specific subjects.
    
    Parameters:
        question_pdf_path (str): Path to the question PDF file.
        answer_pdf_path (str): Path to the answer PDF file.
        show_question (bool, optional): If True, display question PDF; if False, display answer PDF.
    """
    if show_question:
        pdf_type_path = question_pdf_path
        st.write("### Question")
    else:
        pdf_type_path = answer_pdf_path
        st.write("### Answer")

    if pdf_type_path is None:
        st.error("No PDF path provided.")
        return

    try:
        # Handle enhanced resolution for specific subjects
        subjects_to_convert = ['Stats', 'Pure Math']
        doc = fitz.open(pdf_type_path)  # Open the PDF
        zoom = 2  # Higher resolution factor
        mat = fitz.Matrix(zoom, zoom)

        images = [page.get_pixmap(matrix=mat) for page in doc]  # Convert pages to high-res images
        
        if images:
            cols = st.columns(len(images))  # Create columns for each page image
            for i, image in enumerate(images):
                pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
                with cols[i]:
                    st.image(pil_image, caption=f"Page {i + 1}", use_column_width=True)
        else:
            st.warning("No images to display. The PDF might be empty or invalid.")
    except Exception as e:
        st.error(f"Error displaying PDF: {e}")


            
def create_zip(question_path, answer_path):
    """
    Create a ZIP file containing the question and answer PDFs, using BytesIO for in-memory zipping.
    """
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        if os.path.exists(question_path):
            zip_file.write(question_path, os.path.basename(question_path))
        if os.path.exists(answer_path):
            zip_file.write(answer_path, os.path.basename(answer_path))
    zip_buffer.seek(0)
    return zip_buffer

def download_pdf(pdf_paths, zip_name, key):
    """
    Generate a download button for a ZIP containing multiple PDFs.
    """
    # Create the zip in memory
    zip_file = create_zip(pdf_paths[0], pdf_paths[1])  # Assuming pdf_paths contains both question and answer paths
    
    # Create the download button for the zip file
    st.download_button(
        label="Download Question & Answer PDFs",
        data=zip_file,
        file_name=f"{zip_name}.zip",  # Provide the zip file a name
        mime="application/zip",
        key=key  # Ensure unique key for the download button
    )

def display_pdf_quiz(pdf_path, subject_name):
    subjects_to_convert = ['Stats', 'Pure Math']

    doc = fitz.open(pdf_path)  # Open the PDF
    # Improve image quality by increasing resolution
    zoom = 2  # Increase the zoom factor to enhance image quality
    mat = fitz.Matrix(zoom, zoom)  # Apply zoom to transformation matrix
    
    images = [page.get_pixmap(matrix=mat) for page in doc]  # Convert each page to an image at higher resolution

    if subject_name in subjects_to_convert or True:
        if images:
            cols = st.columns(len(images))  # Create columns for the images
            for i, image in enumerate(images):
                pil_image = Image.frombytes("RGB", [image.width, image.height], image.samples)
                with cols[i]:
                    st.image(pil_image, caption=f"Page {i + 1}", use_column_width=True)
        else:
            st.warning("No images to display. The PDF might be empty or invalid.")
    else:
        st.error("Unsupported subject for PDF display.")

def create_zip(question_path, answer_path):
    """Create a ZIP file containing the question and answer PDFs, using BytesIO for in-memory zipping."""
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        if os.path.exists(question_path):
            zip_file.write(question_path, os.path.basename(question_path))
        if os.path.exists(answer_path):
            zip_file.write(answer_path, os.path.basename(answer_path))
    zip_buffer.seek(0)
    return zip_buffer

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
