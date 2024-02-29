# Importing pandas
import pandas as pd
import os
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime
import re

# Path to the CSV file
csv_file_path = '/Users/karthikbalasubramanian/Downloads/SD-22/sd22_targeting.csv'

# Read the CSV file into a DataFrame
sd22_df = pd.read_csv(csv_file_path)

# Now, sd22_df contains the data from the CSV file
# Assuming sd22_df is your DataFrame containing voting records for SD-22

# List of specified precincts
specified_precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Normalize 'vtd_desc' values by removing leading zeros for comparison purposes if they are all numeric
# This step might be optional based on your data format
sd22_df['vtd_desc_norm'] = sd22_df['vtd_desc'].apply(lambda x: x.lstrip('0') if x.isdigit() else x)

for precinct in specified_precincts:
    # Filter all the voting records for the current precinct
    current_precinct_df = sd22_df[sd22_df['vtd_desc_norm'] == precinct]
    
    # Construct the file path for the current precinct
    file_path = f'/Users/karthikbalasubramanian/Downloads/SD-22/Voters/sd22_{precinct}_targeting.csv'
    
    # Save the filtered DataFrame to a CSV file
    current_precinct_df.to_csv(file_path, index=False)

    print(f"CSV for precinct {precinct} saved to {file_path}")

## Make latex table for each precinct

# Function to escape LaTeX special characters in strings
def escape_latex(s):
    """Escape LaTeX special characters in a string."""
    return s.replace('&', '\\&').replace('%', '\\%').replace('$', '\\$')\
            .replace('#', '\\#').replace('_', '\\_').replace('{', '\\{')\
            .replace('}', '\\}').replace('~', '\\textasciitilde{}')\
            .replace('^', '\\textasciicircum{}').replace('\\', '\\textbackslash{}')

# Function to extract and escape just the street name from the address
def extract_and_escape_street_name(address):
    address = address.strip().upper()  # Normalize the address
    street_name = re.sub(r'\b\d+\b', '', address)  # Remove numbers
    street_name = re.sub(r'\s+#.*', '', street_name)  # Remove apartment/unit numbers
    street_name = re.sub(r'\s+\d+.*', '', street_name)  # Remove trailing numbers and suffixes
    street_name = street_name.strip()  # Final cleanup
    return escape_latex(street_name)  # Escape LaTeX special characters

def generate_precinct_latex_table(data, precinct, output_filename):
    output_path = f'/Users/karthikbalasubramanian/Downloads/SD-22/LaTeX/{output_filename}'
    
    # Convert data to LaTeX code without the 'highlight' column
    latex_code = data.to_latex(index=False, column_format='|l|rrr|', escape=False, header=False)
    
    # Split the LaTeX code by lines for manipulation
    lines = latex_code.split('\n')
    
    # Find the line with the precinct data and add the \rowcolor{yellow} command before it
    for i, line in enumerate(lines):
        if precinct in line:
            lines[i] = '\\rowcolor{yellow} ' + line
            break  # Assuming only one row per precinct, we can break after finding the match
    
    # Rejoin the modified lines back into a single string
    modified_latex_code = '\n'.join(lines)
    
    # Write the modified LaTeX code to a file
    with open(output_path, 'w') as file:
        file.write(modified_latex_code)
  
# List of precincts to process
precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Base paths for input CSV files and output LaTeX files
base_csv_path = '/Users/karthikbalasubramanian/Downloads/SD-22/Voters/'
base_latex_path = '/Users/karthikbalasubramanian/Downloads/SD-22/LaTeX/'

# Ensure the output directory exists
os.makedirs(base_latex_path, exist_ok=True)

# Loop through each precinct and generate its LaTeX table with the row highlighted
for precinct in specified_precincts:
    precinct_filename = f'Precincts_Crosstab_{precinct}.tex'
    generate_precinct_latex_table(precinct_universe_counts, precinct, precinct_filename)
    
    # Full paths for input and output
    csv_file_path = os.path.join(base_csv_path, csv_file)
    latex_file_path = os.path.join(base_latex_path, latex_file)

    # Generate the LaTeX table
    generate_latex_table(csv_file_path, latex_file_path)

    print(f'LaTeX table for precinct {precinct} has been generated at {latex_file_path}')

### Precinct table

# Filter for Universes A, B, and C
abc_data = sd22_df[sd22_df['Universe'].isin(['A', 'B', 'C'])]

# Aggregate data by precinct and Universe
precinct_universe_counts = abc_data.groupby(['vtd_desc', 'Universe']).size().unstack(fill_value=0).reset_index()

# Ensure all Universes A, B, and C columns are present
for universe in ['A', 'B', 'C']:
    if universe not in precinct_universe_counts.columns:
        precinct_universe_counts[universe] = 0

# Sort by precinct for consistency
precinct_universe_counts.sort_values(by='vtd_desc', inplace=True)

def generate_precinct_latex_table(data, precinct, output_filename):
    output_path = f'/Users/karthikbalasubramanian/Downloads/SD-22/LaTeX/{output_filename}'

    # Convert the precinct number to a string and ensure it matches the LaTeX format
    precinct_str = str(precinct).lstrip('0')  # Remove leading zeros for matching

    # Convert data to LaTeX code with headers
    latex_code = data.to_latex(index=False, column_format='|l|rrr|', escape=False, header=['Precinct', 'A', 'B', 'C'])

    # Split the LaTeX code by lines for manipulation
    lines = latex_code.split('\n')

    # Iterate over lines to find the exact match for the precinct row
    for i, line in enumerate(lines):
        # Check if the line starts with the precinct number followed by " &" (LaTeX column separator)
        if line.strip().startswith(f'{precinct_str} &'):
            # Add the \rowcolor{yellow} command to highlight the row
            lines[i] = '\\rowcolor{yellow} ' + line
            break  # Found the correct row, no need to continue

    # Rejoin the modified lines back into a single string
    modified_latex_code = '\n'.join(lines)

    # Write the modified LaTeX code to the output file
    with open(output_path, 'w') as file:
        file.write(modified_latex_code)
        
# Loop through each precinct and generate its LaTeX table with the row highlighted
for precinct in specified_precincts:
    generate_precinct_latex_table(precinct_universe_counts, precinct, f'Precincts_Crosstab_{precinct}.tex')

### Early vote adder

import pandas as pd

# Path to the SD-22 CSV file
csv_file_path = '/Users/karthikbalasubramanian/Downloads/SD-22/sd22_targeting.csv'

# Read the SD-22 CSV file into a DataFrame
sd22_df = pd.read_csv(csv_file_path)

# Path to the early voting data CSV file
file_path = '/Users/karthikbalasubramanian/Downloads/absentee_county_20240305/DURHAM_absentee_20240305.csv'

try:
    # Load the early voting data
    earlyvoting = pd.read_csv(file_path, encoding='ISO-8859-1', usecols=['ncid', 'ballot_req_type'])
    print("Early voting data loaded successfully. Here are the first few rows:")
    print(earlyvoting.head())
    
    # Merging 'ballot_req_type' into sd22_df based on 'ncid', using a left join
    merged_df = pd.merge(sd22_df, earlyvoting, on='ncid', how='left')
    
    print("Merged DataFrame head:")
    print(merged_df.head())
    
except Exception as e:
    print(f"An error occurred: {e}")

merged_df['ballot_req_type'].fillna('Not yet Voted', inplace=True)

# Now, generate the crosstab of 'Universe' and 'ballot_req_type' including the "Not yet Voted" category
crosstab_result = pd.crosstab(merged_df['Universe'], merged_df['ballot_req_type'])

print(crosstab_result)

pd.set_option('display.max_rows', None)  # Adjust as necessary
pd.set_option('display.max_columns', None)  # Adjust as necessary

# Calculate the percentage of each universe category (row-wise) that falls into each voting status,
# round the result to the nearest percent, and rename categories
percentage_crosstab_rowwise = crosstab_result.apply(lambda x: (x / x.sum() * 100).round(0), axis=1)
percentage_crosstab_rowwise = percentage_crosstab_rowwise.rename(columns={"EARLY VOTING": "Early In-Person", "MAIL": "Mail", "Not yet Voted": "Not Yet Voted"})

# Convert the numbers to strings and append the '%' symbol
percentage_crosstab_rowwise = percentage_crosstab_rowwise.applymap(lambda x: f"{int(x)}%")

# Transpose the DataFrame for better readability
percentage_crosstab_rowwise_transposed = percentage_crosstab_rowwise.transpose()

latex_table = percentage_crosstab_rowwise_transposed.to_latex(index=True, header=True)

# Generate the filename with today's date
filename = f"Early_Vote_{datetime.now().strftime('%Y%m%d')}.tex"

# Assuming percentage_crosstab_rowwise_transposed is your final DataFrame prepared for LaTeX output
percentage_crosstab_rowwise_transposed.to_latex(filename, index=True, header=True)


merged_df['ballot_req_type'] = merged_df['ballot_req_type'].replace({
    'EARLY VOTING': 'Early In-Person',
    'MAIL': 'Mail',
    # Ensure any NaN or missing values are handled if "Not Yet Voted" is needed
}).fillna('Not Yet Voted')

# Generate the crosstab of raw counts
raw_crosstab = pd.crosstab(merged_df['Universe'], merged_df['ballot_req_type'])

transposed_raw_crosstabb = transpose(raw_crosstab)

# Generate the filename with today's date
filename = f"Early_Vote_raw_{datetime.now().strftime('%Y%m%d')}.tex"

# Assuming percentage_crosstab_rowwise_transposed is your final DataFrame prepared for LaTeX output
transposed_raw_crosstabb.to_latex(filename, index=True, header=True)

# First, mark rows where a vote has occurred (either "Early In-Person" or "Mail")
merged_df['Voted'] = merged_df['ballot_req_type'].apply(lambda x: 'Voted' if x in ['Early In-Person', 'Mail'] else 'Not Yet Voted')

# Generate the crosstab showing the percentage of 'Voted' for each 'Universe' category across precincts
vote_percents = pd.crosstab(merged_df['precinct_desc'], merged_df['Universe'], values=merged_df['Voted'] == 'Voted', aggfunc='mean') * 100

# To sort the table by the largest percentage of "A"s not yet voted, we first need to calculate the "Not Yet Voted" percentages
not_voted_percents = pd.crosstab(merged_df['precinct_desc'], merged_df['Universe'], values=merged_df['Voted'] == 'Not Yet Voted', aggfunc='mean') * 100

# Sort 'vote_percents' by 'A' in 'not_voted_percents' in descending order to have precincts with the highest percentage of "A"s not yet voted at the top
sorted_vote_percents = vote_percents.loc[not_voted_percents['A'].sort_values(ascending=False).index]

sorted_vote_percents_str = sorted_vote_percents.applymap(lambda x: f"{x}%")


###

# Calculate the percentage of 'Not Voted' for each 'Universe' category across 'precinct_desc'
not_voted_percentage = pd.crosstab(merged_df['precinct_desc'], merged_df['Universe'], values=merged_df['Voted'] == 'Not Voted', aggfunc='mean') * 100

# Round to nearest percent and remove decimals
not_voted_percentage_rounded = not_voted_percentage.round(0).astype(int)

# Sort by the percentage of "A"s not yet voted in descending order
sorted_not_voted_percentage = not_voted_percentage_rounded.sort_values(by='A', ascending=False)

print("Percentage of Not Yet Voted by Universe and Precinct:")
print(sorted_not_voted_percentage)

# Generate the filename with today's date
filename = f"Early_Vote_precinct_pct_{datetime.now().strftime('%Y%m%d')}.tex"

# to latex
sorted_not_voted_percentage.to_latex(filename, index=True, header=True)


# Create a 'Not Voted' column for raw count calculation
merged_df['Not Voted'] = merged_df['Voted'].apply(lambda x: 1 if x == 'Not Voted' else 0)

# Calculate the raw number of 'Not Voted' for each 'Universe' category across 'precinct_desc'
raw_not_voted_counts = pd.crosstab(merged_df['precinct_desc'], merged_df['Universe'], values=merged_df['Not Voted'], aggfunc='sum')

# Sort by the raw number of "A"s not yet voted in descending order
sorted_raw_not_voted_counts = raw_not_voted_counts.sort_values(by='A', ascending=False)

print("Raw Number of Not Yet Voted by Universe and Precinct:")
print(sorted_raw_not_voted_counts)

# Generate the filename with today's date
filename = f"Early_Vote_precinct_raw_{datetime.now().strftime('%Y%m%d')}.tex"

# to latex
sorted_raw_not_voted_counts.to_latex(filename, index=True, header=True)

