import os
import shutil

def combine_folders(input_folder1, input_folder2, output_folder):
    # List all subdirectories in both folders
    subfolders_1 = {os.path.relpath(os.path.join(root, subfolder), input_folder1) 
                    for root, dirs, files in os.walk(input_folder1) for subfolder in dirs}
    subfolders_2 = {os.path.relpath(os.path.join(root, subfolder), input_folder2) 
                    for root, dirs, files in os.walk(input_folder2) for subfolder in dirs}
    
    # Combine the subdirectories from both folders
    all_subfolders = subfolders_1.union(subfolders_2)

    # Ensure the output directory exists
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Copy the folders and their contents to the output folder
    for subfolder in all_subfolders:
        # Define the source paths from both input directories
        source1 = os.path.join(input_folder1, subfolder)
        source2 = os.path.join(input_folder2, subfolder)
        
        # Define the target path in the output folder
        target = os.path.join(output_folder, subfolder)

        # Create the target subfolder if it doesn't exist
        if not os.path.exists(target):
            os.makedirs(target)

        # Copy the contents from the source directories to the target
        if os.path.exists(source1):
            for item in os.listdir(source1):
                s = os.path.join(source1, item)
                d = os.path.join(target, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)
        
        if os.path.exists(source2):
            for item in os.listdir(source2):
                s = os.path.join(source2, item)
                d = os.path.join(target, item)
                if os.path.isdir(s):
                    shutil.copytree(s, d, dirs_exist_ok=True)
                else:
                    shutil.copy2(s, d)

# Define the paths for the input folders (OUTPUT_QUESTIONS and TEMP) and output folder
desktop = os.path.expanduser("~/Desktop")
input_folder1 = os.path.join(desktop, '9709')
input_folder2 = os.path.join(desktop, 'trial')
output_folder = os.path.join(desktop, 'ms')

combine_folders(input_folder1, input_folder2, output_folder)
