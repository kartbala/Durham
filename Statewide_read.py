# * Level 1 Header: Imports

# Importing pandas
import pandas as pd
import os
from fuzzywuzzy import fuzz
import numpy as np


# Define file paths for Excel files with the provided path
statewide_voters = '/Users/karthikbalasubramanian/Downloads/SD-22/ncvoter_Statewide.txt'  # Updated with the actual path
statewide_history = '/Users/karthikbalasubramanian/Downloads/SD-22/ncvhis_Statewide.txt'  # Updated with the actual path

# Read the file
try:
    voters_df = pd.read_csv(statewide_voters, sep='\t', encoding='ISO-8859-1')
    print("Statewide Voters Data:")
    print(voters_df.head())
except Exception as e:
    print(f"Error reading voters file: {e}")

# Convert 'nc_senate_abbrv' to string for comparison
voters_df['nc_senate_abbrv'] = voters_df['nc_senate_abbrv'].astype(str)

# Filter the DataFrame to keep only records in Senate District 22
# Since the column is now a string, we compare with the string '22.0'
senate_district_22_df = voters_df[voters_df['nc_senate_abbrv'] == '22.0']

# Now senate_district_22_df contains only the records for Senate District 22
print(senate_district_22_df.head())

## * Latex table for party affiilations

# Group by 'party_cd' and count records in each group
party_counts = senate_district_22_df['party_cd'].value_counts()

# Sort the party counts in descending order
party_counts = party_counts.sort_values(ascending=False)

# Generate LaTeX table
latex_table = "\\begin{tabular}{|c|c|}\n"
latex_table += "\\hline\n"
latex_table += "Party & Frequency \\\\\n"
latex_table += "\\hline\n"

for party, count in party_counts.items():
    latex_table += f"{party} & {count} \\\\\n"

latex_table += "\\hline\n"
latex_table += "\\end{tabular}"

## * Print the LaTeX table
print(latex_table)

# * Filter out all non-dem/non-unaffiliated_data

# Filter for 'DEM' and 'UNA' parties
filtered_df = senate_district_22_df[senate_district_22_df['party_cd'].isin(['DEM', 'UNA'])]

# Save the combined dataset to the specified CSV file
filtered_df.to_csv("~/Downloads/SD-22/sd22_eligible.csv", index=False)

bsa_matched = pd.read_csv('~/Downloads/SD-22/bsa_matched.csv')
bsa_matched = bsa_matched.rename(columns={"NCID": "ncid"})

# Inner join on 'ncid' column
intersection_df = pd.merge(bsa_matched, filtered_df, how='inner', on='ncid')
# Apply fuzz.ratio to each row
intersection_df['similarity_score'] = intersection_df.apply(lambda row: fuzz.ratio(row['Name'], row['Registered Name'])/100, axis=1)

import matplotlib.pyplot as plt

plt.hist(intersection_df['similarity_score'], bins=10, alpha=0.7)
plt.title('Histogram of Similarity Scores')
plt.xlabel('Similarity Score')
plt.ylabel('Frequency')
plt.grid(True)
plt.show()

# To save intersection_df to new CSV file
intersection_df.to_csv('intersection_df.csv', index=False)


# Now, filtered_df contains only rows with 'DEM' and 'UNA' parties
print(filtered_df.head())

* now add history

# Read the file
try:
    history_df = pd.read_csv("/Users/karthikbalasubramanian/Downloads/SD-22/ncvhis_Statewide.txt", sep='\t', encoding='ISO-8859-1')
    print("Statewide Voters Data:")
    print(history_df.head())
except Exception as e:
    print(f"Error reading voters file: {e}")

# throw away all the non-sd22

# Extract the voter registration numbers from 'filtered_df'
filtered_voter_reg_nums = sd22_df['ncid']

# Filter 'voter_df' to keep only rows with voter registration numbers present in 'filtered_df'
sd22_history_df = history_df[history_df['ncid'].isin(filtered_voter_reg_nums)]

sd22_df['registr_dt'] = pd.to_datetime(sd22_df['registr_dt'])
sd22_df['year'] = sd22_df['registr_dt'].dt.year

# Merge registration date into sd22_history_df
sd22_history_df = pd.merge(sd22_history_df, sd22_df[['ncid', 'registr_dt']], on='ncid', how='left')

# Assuming sd22_history_df and sd22_df are your DataFrames
# Replace 'sd22_history_df' and 'sd22_df' with your actual DataFrame names if they're different

# Define the mapping of 'election_desc' to new column names
election_mapping = {
    "11/03/2020 GENERAL": "G20",
    "11/08/2016 GENERAL": "G16",
    "11/08/2022 GENERAL": "G22",
    "11/06/2018 GENERAL": "G18",
    "03/03/2020 PRIMARY": "P20",
    "03/15/2016 PRIMARY": "P16",
    "05/17/2022 PRIMARY": "P22",
    "11/07/2023 MUNICIPAL": "G23",
    "05/08/2018 PRIMARY": "P18",
    "11/05/2019 MUNICIPAL ELECTION": "G19",
    "11/07/2017 MUNICIPAL ELECTION": "G17",
    "11/02/2021 MUNICIPAL ELECTION": "G21",
    "10/10/2023 PRIMARY": "P23",
    "10/10/2017 MUNICIPAL PRIMARY": "P17",
    "10/05/2021 MUNICIPAL PRIMARY": "P21",
    "10/08/2019 MUNICIPAL PRIMARY": "P19"
}

# Make sure 'ncid' is a column, not an index in both DataFrames
sd22_history_df.reset_index(drop=True, inplace=True)
sd22_df.reset_index(drop=True, inplace=True)

# Transform 'election_desc' into a column that reflects the new column names
sd22_history_df['election_col'] = sd22_history_df['election_desc'].map(election_mapping)

# Create a pivot table with 'ncid' as index and the new election columns
pivot_df = sd22_history_df.pivot_table(index='ncid', 
                                       columns='election_col', 
                                       aggfunc='size', 
                                       fill_value=0)


# Reset index to make 'ncid' a column again
pivot_df.reset_index(inplace=True)

# Merge the pivot table with sd22_df
sd22_df = sd22_df.merge(pivot_df, on='ncid', how='left')

# Replace NaN values with 0 if there are any after merging
sd22_df.fillna(0, inplace=True)

# Convert the new column values to int
for col in election_mapping.values():
    if col in sd22_df.columns:
        sd22_df[col] = sd22_df[col].astype(int)



        
        
# Extract year and date from 'election_lbl'
sd22_history_df['election_date'] = pd.to_datetime(sd22_history_df['election_lbl'].str[-10:], format='%m/%d/%Y')

# Filter sd22_history_df by registration date
sd22_history_df = sd22_history_df[sd22_history_df['election_date'] >= sd22_history_df['registr_dt']]

sd22_history_df = sd22_history_df.reset_index()

def tabulate_even_year_primaries(df):
    df['election_desc_primary'] = df['election_desc'].apply(lambda x: 'PRIMARY' in x)
    df['election_date'] = pd.to_datetime(df['election_lbl'].str[-10:], format='%m/%d/%Y')
    df['election_year_even'] = df['election_date'].dt.year.apply(lambda x: x % 2 == 0)
    df['even_year_primaries'] = df['election_desc_primary'] & df['election_year_even']
    return df

sd22_history_df = sd22_history_df.groupby('ncid').apply(tabulate_even_year_primaries)

summary = sd22_history_df.groupby('ncid').agg(
    total_elections=('election_lbl', 'count'),
    primary_elections=('election_desc_primary', sum),
    even_primary_elections=('even_year_primaries', sum)
)


sd22_history_df = sd22_history_df.reset_index()

def tabulate_even_year_primaries(df):
    df['election_desc_primary'] = df['election_desc'].apply(lambda x: 'PRIMARY' in x)
    df['election_date'] = pd.to_datetime(df['election_lbl'].str[-10:], format='%m/%d/%Y')
    df['election_year_even'] = df['election_date'].dt.year.apply(lambda x: x % 2 == 0)
    df['even_year_primaries'] = df['election_desc_primary'] & df['election_year_even']
    return df

sd22_history_df = sd22_history_df.groupby('ncid').apply(tabulate_even_year_primaries)

summary = sd22_history_df.groupby('ncid').agg(
    total_elections=('election_lbl', 'count'),
    primary_elections=('election_desc_primary', sum),
    even_primary_elections=('even_year_primaries', sum)
)


def tabulate_even_year_primaries(df):
    df['election_desc_primary'] = df['election_desc'].apply(lambda x: 'PRIMARY' in x)
    df['election_date'] = pd.to_datetime(df['election_lbl'].str[-10:], format='%m/%d/%Y')
    df['election_year_even'] = df['election_date'].dt.year.apply(lambda x: x % 2 == 0)
    df['even_year_primaries'] = df['election_desc_primary'] & df['election_year_even']
    return df

sd22_history_df = sd22_history_df.groupby('ncid').apply(tabulate_even_year_primaries)

summary = sd22_history_df.groupby('ncid').agg(
    total_elections=('election_lbl', 'count'),
    primary_elections=('election_desc_primary', sum),
    even_primary_elections=('even_year_primaries', sum)
)

# Reset index before merge
summary = summary.reset_index()

summary = pd.merge(sd22_df[['ncid']], summary, on='ncid', how='left')
summary[['total_elections', 'primary_elections', 'even_primary_elections']] = summary[['total_elections', 'primary_elections', 'even_primary_elections']].fillna(0)

def derive_category(row):
    if row['total_elections'] == 0:
        return 'Never voted'
    elif row['primary_elections'] == 0:
        return 'Has voted but never in a primary since reg'
    elif row['even_primary_elections'] > 0 < row['primary_elections']:
        return 'Voted in some but not all even-year primaries'
    elif row['even_primary_elections'] > 0 == row['primary_elections']:
        return 'Voted in All even-year primaries but not all primaries'
    else:
        return 'Voted in All primaries since reg'

summary['voting_category'] = np.vectorize(derive_category)(summary)

# throw away everything before 2016

# Convert the 'election_lbl' column to datetime format
filtered_history_df['election_lbl'] = pd.to_datetime(filtered_history_df['election_lbl'], format='%m/%d/%Y')

# Filter out rows where 'election_lbl' is before 2016
filtered_history_df = filtered_history_df[filtered_history_df['election_lbl'].dt.year >= 2016]

# fitler out the small elections

# List of desired 'election_desc' values
desired_election_desc = [
    '11/03/2020 GENERAL',
    '11/08/2016 GENERAL',
    '11/08/2022 GENERAL',
    '11/06/2018 GENERAL',
    '03/03/2020 PRIMARY',
    '03/15/2016 PRIMARY',
    '05/17/2022 PRIMARY',
    '05/08/2018 PRIMARY'
]

# Assuming you have a DataFrame named 'filtered_history_df'

# Filter out rows where 'election_desc' is in the desired list
filtered_history_df = filtered_history_df[filtered_history_df['election_desc'].isin(desired_election_desc)]

# throw away anywith a voted_party_cd not DEM or UNA


# List of desired 'voted_party_cd' values
desired_party_cd = ['DEM', 'UNA']

# Assuming you have a DataFrame named 'filtered_history_df'

# Filter out rows where 'voted_party_cd' is in the desired list
filtered_history_df = filtered_history_df[filtered_history_df['voted_party_cd'].isin(desired_party_cd)]


# 'filtered_history_df' now contains only rows with 'election_desc' in the desired list

# Merge 'filtered_df' and 'history_df' based on the 'voter_reg_num' column
merged_df = pd.merge(filtered_df, voters_df, on='voter_reg_num', how='left')

# 'merged_df' now contains the merged data based on the 'voter_reg_num' column



# Sort the party counts in descending order
party_counts = party_counts.sort_values(ascending=False)

# Generate LaTeX table
latex_table = "\\begin{tabular}{|c|c|}\n"
latex_table += "\\hline\n"
latex_table += "Party & Frequency \\\\\n"
latex_table += "\\hline\n"

for party, count in party_counts.items():
    latex_table += f"{party} & {count} \\\\\n"

latex_table += "\\hline\n"
latex_table += "\\end{tabular}"

# Print the LaTeX table
print(latex_table)



# Read the voters file (assuming tab-delimited; adjust as needed)
try:
    voters_df = pd.read_csv(statewide_voters, sep='\t', encoding='utf-8')
    print("Statewide Voters Data:")
    print(voters_df.head())
except Exception as e:
    print(f"Error reading voters file: {e}")

# Read the history file (assuming tab-delimited; adjust as needed)
try:
    history_df = pd.read_csv(statewide_history, sep='\t', encoding='utf-8')
    print("\nStatewide History Data:")
    print(history_df.head())
except Exception as e:
    print(f"Error reading history file: {e}")

# Filter for NC Senate District 22 and Active Status
democrats_filtered = democrats_data[(democrats_data['NC Senate District'] == 22) & (democrats_data['Status'] == 'A')]
unaffiliated_filtered = unaffiliated_data[(unaffiliated_data['NC Senate District'] == 22) & (unaffiliated_data['Status'] == 'A')]

# Concatenate the filtered dataframes
combined_active_data = pd.concat([democrats_filtered, unaffiliated_filtered], ignore_index=True)

output_file = '/Users/karthikbalasubramanian/Downloads/SD-22/CombinedActiveVoters_District22.csv'

# Save the combined dataset to the specified CSV file
combined_active_data.to_csv(output_file, index=False)

