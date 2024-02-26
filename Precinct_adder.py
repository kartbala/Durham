import pandas as pd

# Define the paths to your CSV files
contacts_csv_path = '/Users/karthikbalasubramanian/Downloads/People\'s Alliance - Sheet1.csv'
sd22_csv_path = '/Users/karthikbalasubramanian/Downloads/SD-22/sd22_eligible.csv'

# Load the CSV files into DataFrames
contacts_df = pd.read_csv(contacts_csv_path)
sd22_df = pd.read_csv(sd22_csv_path, low_memory=False)

# Rename columns in contacts_df for merging, and convert names to lowercase for case-insensitive matching
contacts_df_renamed = contacts_df.rename(columns={'Last Name': 'last_name', 'First Name': 'first_name'})
contacts_df_renamed['last_name'] = contacts_df_renamed['last_name'].str.lower()
contacts_df_renamed['first_name'] = contacts_df_renamed['first_name'].str.lower()

# Convert names in sd22_df to lowercase for case-insensitive matching
sd22_df['last_name'] = sd22_df['last_name'].str.lower()
sd22_df['first_name'] = sd22_df['first_name'].str.lower()

# Perform the merge to add the 'vtd_desc' column from sd22_df to contacts_df
merged_df = pd.merge(contacts_df_renamed, sd22_df[['last_name', 'first_name', 'vtd_desc']], 
                     on=['last_name', 'first_name'], 
                     how='left')

# Fill in "no match" where vtd_desc is NaN
merged_df['vtd_desc'].fillna('no match', inplace=True)

# Example: Find the vtd_desc for Benjamin Abram
benjamin_abram_entry = merged_df[(merged_df['first_name'] == 'benjamin') & 
                                 (merged_df['last_name'] == 'abram')]
print(benjamin_abram_entry[['last_name', 'first_name', 'vtd_desc']])

# Example: Find the vtd_desc for Trudi Abel
trudi_abel_entry = merged_df[(merged_df['first_name'] == 'trudi') & 
                             (merged_df['last_name'] == 'abel')]
print(trudi_abel_entry[['last_name', 'first_name', 'vtd_desc']])

merged_df.to_csv('/Users/karthikbalasubramanian/Downloads/SD-22/PA_matching_for_J.csv', index=False)
