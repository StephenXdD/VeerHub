import os
import re
import shutil

def rename_pdfs_in_temp():
    # Define paths to TEMP and trial_output folders on the desktop
    desktop = os.path.expanduser("~/Desktop")
    temp_folder = os.path.join(desktop, "TEMP")
    output_folder = os.path.join(desktop, "trial_output")
    
    # Map of old numbers to new numbers for renaming
    rename_map = {
        "6": "5",
        "61": "51",
        "62": "52",
        "63": "53"
    }
    
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)
    
    # Pattern to identify and capture the part of the name to replace
    pattern = re.compile(r"_(6|61|62|63)(?=_cleaned\.pdf$)")
    
    # Process each file in the TEMP folder
    for filename in os.listdir(temp_folder):
        if filename.endswith("_cleaned.pdf"):
            # Find the match and replace according to rename_map
            match = pattern.search(filename)
            if match:
                old_number = match.group(1)
                new_number = rename_map.get(old_number)
                
                # Create the new filename with the replaced number
                new_filename = filename.replace(f"_{old_number}_", f"_{new_number}_")
                
                # Define the full paths for original and new file
                old_path = os.path.join(temp_folder, filename)
                new_path = os.path.join(output_folder, new_filename)
                
                # Copy the file to the output folder with the new name
                try:
                    shutil.copy2(old_path, new_path)
                    print(f"Renamed '{filename}' to '{new_filename}'")
                except Exception as e:
                    print(f"Error renaming '{filename}': {e}")

rename_pdfs_in_temp()
