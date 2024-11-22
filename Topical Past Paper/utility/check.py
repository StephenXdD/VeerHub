import os
import glob

def check_pdfs_in_subdirectories(directory):
    # Traverse all subdirectories of 'output_questions'
    for subdir, dirs, files in os.walk(directory):
        # Find all PDF files in the subdirectory
        pdf_files = glob.glob(os.path.join(subdir, '*.pdf'))
        
        # If there are PDF files in the subdirectory
        if pdf_files:
            # Check if the number of PDFs is not 40
            if len(pdf_files) != 4:
                print(f"Warning: The subdirectory '{subdir}' does not contain 4 PDFs, it contains {len(pdf_files)}.")
            else:
                print(f"Subdirectory '{subdir}' contains 4 PDFs.")
                
# Set the path of your main directory
main_directory = 'output_questions'

# Call the function
check_pdfs_in_subdirectories(main_directory)
