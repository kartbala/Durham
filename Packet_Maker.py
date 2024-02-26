# Importing pandas
import subprocess
import pandas as pd
import os
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime

import os

# List of specified precincts with single-digit numbers not padded with a leading zero
specified_precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Base path where the .tex files are located
base_path = '/Users/karthikbalasubramanian/Downloads/SD-22/Latex/'
tex_files_directory = base_path 

# Read the content of 10.tex
with open(os.path.join(base_path, '10.tex'), 'r') as file:
    content = file.read()

# Loop through the specified precincts
for precinct in specified_precincts:
    # Normalize the precinct number to ensure it's zero-padded to two digits if necessary
    # Split precincts like "30-2" to handle them separately
    precinct_parts = precinct.split('-')
    for part in precinct_parts:
        precinct_number = part.zfill(2)  # Zero-pad to two digits

        # Generate the filename for the new .tex file
        new_filename = f'{precinct_number}.tex'

        # Write the content to the new file
        with open(os.path.join(base_path, new_filename), 'w') as new_file:
            new_file.write(content)

    print(f'Created {new_filename} as a copy of 10.tex')

### Deal with the leading 0 problem

# Directory where your .tex files are stored
directory = '/Users/karthikbalasubramanian/Downloads/SD-22/LaTeX/'

# List all .tex files in the directory
tex_files = [f for f in os.listdir(directory) if f.endswith('.tex')]

for filename in tex_files:
    # Skip files that don't follow the 'Precincts_Crosstab_X.tex' naming convention
    if 'Crosstab' not in filename:
        continue

    # Split the filename to isolate the precinct number part
    parts = filename.split('_')
    print(parts)

    # Ensure that parts has at least three elements before proceeding
    if len(parts) >= 3 and parts[2].rstrip('.tex').isdigit():
        # Extract the precinct number, stripping off the '.tex' and converting to int
        precinct_number = int(parts[2].rstrip('.tex'))
        
        if precinct_number < 10:
            # Generate the new filename with a leading zero for the precinct number
            new_filename = f"{parts[0]}_{parts[1]}_0{precinct_number}.tex"
        else:
            # For precinct numbers 10 and above, no change is needed
            new_filename = filename

        # Construct the full paths for the old and new filenames
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)

        # Rename the file if the new filename is different
        if new_filename != filename:
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_filename}'")


# Directory where your PDF files are stored
directory = '/Users/karthikbalasubramanian/Downloads/SD-22/Maps'

# List all PDF files in the directory
pdf_files = [f for f in os.listdir(directory) if f.endswith('.pdf')]

for filename in pdf_files:
    # Skip files that don't follow the 'Highlighted_Precinct_X.pdf' naming convention
    if not filename.startswith('Highlighted_Precinct_'):
        continue

    # Split the filename to isolate the precinct number part
    parts = filename.split('_')
    
    # Since the precinct number is the third part, check if it's a digit and needs zero-padding
    precinct_part = parts[2].rstrip('.pdf')  # Remove '.pdf' to get just the number part
    if precinct_part.isdigit():
        precinct_number = int(precinct_part)
        if precinct_number < 10:
            # Generate the new filename with a leading zero for the precinct number
            new_filename = f"{parts[0]}_{parts[1]}_0{precinct_number}.pdf"
        else:
            new_filename = filename  # No change needed for two-digit numbers

        # Construct the full paths for the old and new filenames
        old_file = os.path.join(directory, filename)
        new_file = os.path.join(directory, new_filename)

        # Rename the file if the new filename is different from the original
        if new_filename != filename:
            os.rename(old_file, new_file)
            print(f"Renamed '{filename}' to '{new_filename}'")
            
            
### Compile the tex files    

for tex_file in tex_files:
    # Remove the extension and replace non-digit characters to check if the filename contains only digits
    filename_without_extension = tex_file[:-4]  # Remove the '.tex' extension
    filename_digits_only = filename_without_extension.replace('_', '').replace('-', '')

    # Check if the modified filename contains only digits
    if filename_digits_only.isdecimal():
        # Construct the full path to the .tex file
        full_tex_file_path = os.path.join(tex_files_directory, tex_file)
        
        # Compile the .tex file using pdflatex
        subprocess.run(['pdflatex', '-output-directory', tex_files_directory, full_tex_file_path])

        print(f'Compiled: {tex_file}')
    else:
        print(f'Skipped: {tex_file} (contains alphabetical characters)')

### Copy to GOogle Drive

import shutil
import os

# Directory where your LaTeX-generated PDF files are stored
source_directory = '/Users/karthikbalasubramanian/Downloads/SD-22/LaTeX/'

# Destination directory where you want to copy the PDFs
destination_directory = '/Users/karthikbalasubramanian/My Drive/SD-22/Precinct_Strategy_Docs/'

# Ensure the destination directory exists, create it if it doesn't
os.makedirs(destination_directory, exist_ok=True)

# List all files in the source directory
files = os.listdir(source_directory)

# Loop through the files and copy if they are PDFs
for file in files:
    if file.endswith('.pdf'):
        # Construct the full path to the source and destination files
        source_file = os.path.join(source_directory, file)
        destination_file = os.path.join(destination_directory, file)

        # Copy the PDF file from the source to the destination
        shutil.copy2(source_file, destination_file)

        print(f'Copied: {file}')
