import os

def rename_folders_in_output_questions():
    # Define the path to the OUTPUT_QUESTIONS folder on the desktop
    desktop = os.path.expanduser("~/Desktop")
    output_questions_path = os.path.join(desktop, "OUTPUT_QUESTIONS")
    
    # Map of old folder names to new folder names
    rename_map = {
        "6": "5",
        "61": "51",
        "62": "52",
        "63": "53"
    }
    
    # Walk through all subdirectories
    for root, dirs, files in os.walk(output_questions_path):
        for dir_name in dirs:
            # Check if the directory name is in the rename map
            if dir_name in rename_map:
                # Define the full old path and the new path with the updated name
                old_path = os.path.join(root, dir_name)
                new_path = os.path.join(root, rename_map[dir_name])
                
                # Rename the directory
                try:
                    os.rename(old_path, new_path)
                    print(f"Renamed '{old_path}' to '{new_path}'")
                except Exception as e:
                    print(f"Error renaming '{old_path}' to '{new_path}': {e}")

rename_folders_in_output_questions()
