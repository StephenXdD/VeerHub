import os

# Path to the "Topical Past Paper" folder on the desktop
folder_path = os.path.expanduser('~/Desktop/Topical Past Paper')

# List to store the names of Python files
python_files = []

# Iterate through the files in the folder
for file_name in os.listdir(folder_path):
    # Check if the file ends with '.py'
    if file_name.endswith('.py'):
        python_files.append(file_name)

# Print the list of Python files
print("Python Files in 'Topical Past Paper' folder:")
for python_file in python_files:
    print(python_file)
