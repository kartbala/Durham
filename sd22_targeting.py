# * Imports

# Importing pandas
import pandas as pd
import os
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime

# Define file paths for Excel files with the provided path
sd22_df = pd.read_csv('~/Downloads/SD-22/sd22_history.csv', dtype={'full_phone_number': str})

# Convert registration date to datetime format
sd22_df['registr_dt'] = pd.to_datetime(sd22_df['registr_dt'])


for election in election_mapping:
    election_date = election_mapping[election]
    # Create a new column for each election. 1 if eligible, 0 otherwise
    sd22_df[election + '_eligible'] = sd22_df['registr_dt'].apply(lambda x: 1 if x <= election_date else 0)

# Election mapping
election_mapping = {
    "G20": "2020-11-03",
    "G16": "2016-11-08",
    "G22": "2022-11-08",
    "G18": "2018-11-06",
    "P20": "2020-03-03",
    "P16": "2016-03-15",
    "P22": "2022-05-17",
    "G23": "2023-11-07",
    "P18": "2018-05-08",
    "G19": "2019-11-05",
    "G17": "2017-11-07",
    "G21": "2021-11-02",
    "P23": "2023-10-10",
    "P17": "2017-10-10",
    "P21": "2021-10-05",
    "P19": "2019-10-08"
}

# Use the keys of the election_mapping dictionary as the column names
voting_columns = list(election_mapping.keys())

# Assign 'E' to everyone with a total vote count of 0 in the 'Total_Votes' column
sd22_df['Universe'] = sd22_df['Total_Votes'].apply(lambda x: 'E' if x == 0 else 'Needs Review')

# Identify primary election columns (assuming they start with 'P')
primary_election_columns = [key for key in election_mapping.keys() if key.startswith('P')]

# Sum the primary election columns for each row
sd22_df['Total_Primary_Votes'] = sd22_df[primary_election_columns].sum(axis=1)

def categorize_voter(row):
    if row['Universe'] != 'E' and row['Total_Primary_Votes'] == 0:
        return 'D'
    else:
        return row['Universe']

# Apply the function to each row
sd22_df['Universe'] = sd22_df.apply(categorize_voter, axis=1)

# Function to categorize each voter
def categorize_voter(row):
    # Count of eligible primaries
    eligible_primaries_count = sum(row[primary + '_eligible'] for primary in primary_election_columns)

    # Count of primaries actually voted in
    voted_primaries_count = sum(row[primary] for primary in primary_election_columns)

    if eligible_primaries_count == voted_primaries_count and eligible_primaries_count > 0:
        return 'A'
    else:
        return row['Universe']  # retain current categorization

# Apply the function to each row
sd22_df['Universe'] = sd22_df.apply(categorize_voter, axis=1)

# Function to check if the year is even
def is_even_year(year):
    return year % 2 == 0

import numpy as np

# Assuming your DataFrame is sd22_df and election_mapping is defined
# Function to check if the year is even
def is_even_year(year):
    return year % 2 == 0

# Identify primary election columns and even-year primary columns
primary_election_columns = [key for key in election_mapping.keys() if 'P' in key]
even_year_primary_columns = [key for key in primary_election_columns if is_even_year(int(key[1:3]))]

# Function to categorize each voter
def categorize_as_B(row):
    # Count of eligible primaries and even-year primaries
    eligible_primaries_count = sum(row[primary + '_eligible'] == 1 for primary in primary_election_columns)
    eligible_even_year_primaries_count = sum(row[primary + '_eligible'] == 1 for primary in even_year_primary_columns)

    # Count of primaries actually voted in
    voted_primaries_count = sum(row[primary] == 1 for primary in primary_election_columns)
    voted_even_year_primaries_count = sum(row[primary] == 1 for primary in even_year_primary_columns)

    # Check conditions for 'B' categorization
    if (eligible_even_year_primaries_count == voted_even_year_primaries_count and 
        eligible_primaries_count > voted_primaries_count):
        return 'B'
    else:
        return row['Universe']  # retain current categorization

# Apply the function to each row
sd22_df['Universe'] = sd22_df.apply(categorize_as_B, axis=1)

# Function to categorize each voter as 'C'
def categorize_as_C(row):
    if row['Universe'] in ['A', 'B', 'D', 'E']:
        # Skip if already categorized as A, B, D, or E
        return row['Universe']

    # Check if voted in some primaries but not all even-year primaries
    voted_in_some_primaries = any(row[primary] == 1 for primary in primary_election_columns)
    not_voted_in_all_even_year_primaries = any(row[primary + '_eligible'] == 1 and row[primary] == 0 for primary in even_year_primary_columns)

    if voted_in_some_primaries and not_voted_in_all_even_year_primaries:
        return 'C'
    else:
        return row['Universe']  # retain current categorization if not C

# Apply the function to each row
sd22_df['Universe'] = sd22_df.apply(categorize_as_C, axis=1)


# Assuming your DataFrame is sd22_df and election_mapping is defined
# Function to check if the year is even
def is_even_year(year):
    return year % 2 == 0

# Identify primary election columns and even-year primary columns
primary_election_columns = [key for key in election_mapping.keys() if 'P' in key]
even_year_primary_columns = [key for key in primary_election_columns if is_even_year(int(key[1:3]))]

# Function to categorize each voter as 'C'
def categorize_as_C(row):
    # Check if voted in at least one eligible primary
    voted_in_at_least_one_primary = any(row[primary] == 1 and row[primary + '_eligible'] == 1 for primary in primary_election_columns)

    # Check if not voted in all eligible even-year primaries
    eligible_even_year_primaries_count = sum(row[primary + '_eligible'] == 1 for primary in even_year_primary_columns)
    voted_even_year_primaries_count = sum(row[primary] == 1 for primary in even_year_primary_columns)
    not_voted_in_all_even_year_primaries = voted_even_year_primaries_count < eligible_even_year_primaries_count

    if voted_in_at_least_one_primary and not_voted_in_all_even_year_primaries:
        return 'C'
    else:
        return row['Universe']  # retain current categorization

# Apply the function to each row
sd22_df['Universe'] = sd22_df.apply(categorize_as_C, axis=1)

sd22_df.to_csv('/Users/karthikbalasubramanian/Downloads/SD-22/sd22_targeting.csv', index=False)
