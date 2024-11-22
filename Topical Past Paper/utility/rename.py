import os
import re
import shutil

def rename_and_copy_pdfs(base_folder, output_folder):
    for root, _, files in os.walk(base_folder):
        for file_name in files:
            if file_name.endswith(".pdf"):
                # Extract the relative path
                relative_path = os.path.relpath(root, base_folder)

                # Construct the destination folder path
                destination_folder = os.path.join(output_folder, relative_path)
                os.makedirs(destination_folder, exist_ok=True)

                # Extract the original file path
                original_file_path = os.path.join(root, file_name)

                # Match and extract the new name using regex
                match = re.match(r"(\d+)(?:\([a-zA-Z]+\)|\([ivx]+\))?\.pdf", file_name)
                if match:
                    new_file_name = f"{match.group(1)}.pdf"
                else:
                    # If no match, keep the original name
                    new_file_name = file_name

                # Construct the new file path
                new_file_path = os.path.join(destination_folder, new_file_name)

                # Copy and rename the file
                if not os.path.exists(new_file_path):
                    shutil.copy2(original_file_path, new_file_path)
                    print(f"Copied and renamed: {original_file_path} -> {new_file_path}")
                else:
                    print(f"Skipped (file already exists): {new_file_path}")

    print("PDF renaming and copying completed.")

# Input and output folders
input_folder = os.path.expanduser("~/Desktop/try")  # Replace with the path to your input folder
output_folder = os.path.expanduser("~/Desktop/renamed_pdfs")  # Replace with the path to your output folder

rename_and_copy_pdfs(input_folder, output_folder)
