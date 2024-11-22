import os
import comtypes.client

# Define the folder containing the .docx files
input_folder = 'WIP'  # Adjust the path to your WIP folder
output_folder = "WIP_PDFs"  # Folder to save PDFs

# Ensure the output folder exists
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Initialize the Word application
word = comtypes.client.CreateObject('Word.Application')
word.Visible = False  # Run Word in the background

# Loop through each file in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith('.docx'):
        docx_path = os.path.join(input_folder, filename)
        pdf_path = os.path.join(output_folder, f'{os.path.splitext(filename)[0]}.pdf')
        
        # Open the .docx file in Word
        doc = word.Documents.Open(docx_path)
        
        # Save it as a PDF
        doc.SaveAs(pdf_path, FileFormat=17)  # FileFormat=17 is for PDFs
        doc.Close()

# Quit the Word application
word.Quit()

print("Conversion complete!")
