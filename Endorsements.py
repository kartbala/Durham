import pandas as pd

# Load the dataset for Satana Deberry
deberry_file_path = '/Users/karthikbalasubramanian/Downloads/2018_DA.csv'
deberry_data = pd.read_csv(deberry_file_path)

# Load the dataset for Steve Schewel
schewel_file_path = '/Users/karthikbalasubramanian/Downloads/2017_Mayor.csv'
schewel_data = pd.read_csv(schewel_file_path)

# Ensure the 'Precinct' column is of type string for both datasets
deberry_data['Precinct'] = deberry_data['Precinct'].astype(str)
schewel_data['Precinct'] = schewel_data['Precinct'].astype(str)

# Pad single-digit precinct numbers with a '0'
deberry_data['Precinct'] = deberry_data['Precinct'].str.zfill(2)
schewel_data['Precinct'] = schewel_data['Precinct'].str.zfill(2)

# Convert percentage columns to numeric, removing any non-numeric characters if necessary
deberry_data['%Satana Deberry'] = pd.to_numeric(deberry_data['%Satana Deberry'].str.replace('%', ''), errors='coerce')
schewel_data['%Steve Schewel'] = pd.to_numeric(schewel_data['%Steve Schewel'].str.replace('%', ''), errors='coerce')

# Merge the two datasets on the 'Precinct' column
merged_data = pd.merge(deberry_data, schewel_data, on='Precinct', suffixes=('_Deberry', '_Schewel'))

# Calculate the performance difference (Schewel - Deberry)
merged_data['Indy_estimate_1'] = merged_data['%Steve Schewel'] - merged_data['%Satana Deberry']

# Display the merged data with the performance difference
print(merged_data[['Precinct', '%Satana Deberry', '%Steve Schewel', 'Indy_estimate_1']])

# Specified precincts, ensuring strings to match potential formatting in the dataset
specified_precincts = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "14", "15", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "28", "29", "30-2", "30-3", "32", "36", "37", "40",
    "43", "44", "45", "46", "50", "52"
]

estimate_1 = merged_data[merged_data['Precinct'].isin(specified_precincts)][['Precinct', '%Satana Deberry', '%Steve Schewel', 'Indy_estimate_1']]

### Estimate 2

import pandas as pd

# Load the data from the specified file path
file_path = '/Users/karthikbalasubramanian/Downloads/Commission_2018.csv'
data = pd.read_csv(file_path)

# Ensure precinct numbers are two digits
data['Precinct'] = data['Precinct'].apply(lambda x: x.zfill(2))

# Convert vote counts to numeric values
columns_to_convert = ['James Hill', 'Elaine C. Hyman']
for column in columns_to_convert:
    data[column] = pd.to_numeric(data[column].str.replace(',', ''), errors='coerce')

# Calculate the total votes per precinct (assuming total votes are the sum of James Hill and Elaine C. Hyman votes)
data['Total Votes'] = data['James Hill'] + data['Elaine C. Hyman']

# Calculate the percentage of votes for each candidate
data['% James Hill'] = (data['James Hill'] / data['Total Votes']) * 100
data['% Elaine C. Hyman'] = (data['Elaine C. Hyman'] / data['Total Votes']) * 100

# Calculate the percentage difference and label it as 'Indy_estimate_2'
data['Indy_estimate_2'] = data['% James Hill'] - data['% Elaine C. Hyman']

# Specify the precincts of interest
specified_precincts = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "14", "15", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "28", "29", "30-2", "30-3", "32", "36", "37", "40",
    "43", "44", "45", "46", "50", "52"
]

# Filter the data for the specified precincts
filtered_data = data[data['Precinct'].isin(specified_precincts)]

# Display the relevant information
estimate_2 = filtered_data[['Precinct', '% James Hill', '% Elaine C. Hyman', 'Indy_estimate_2']]


### Esimate 3

import pandas as pd

# Load the 2020 Commission data
file_path_2020 = '/Users/karthikbalasubramanian/Downloads/2020_Commission.csv'
data_2020 = pd.read_csv(file_path_2020)

# Ensure precinct numbers are in a two-digit format
data_2020['Precinct'] = data_2020['Precinct'].apply(lambda x: str(x).zfill(2))

# Specified precincts, ensuring strings to match potential formatting in the dataset
specified_precincts = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "14", "15", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "28", "29", "30-2", "30-3", "32", "36", "37", "40",
    "43", "44", "45", "46", "50", "52"
]

# Filter the data for the specified precincts
filtered_data_2020 = data_2020[data_2020['Precinct'].isin(specified_precincts)]

# Convert vote counts to numeric values for Nida Allam and Matt Kopac
filtered_data_2020['Nida Allam'] = pd.to_numeric(filtered_data_2020['Nida Allam'].str.replace(',', ''), errors='coerce')
filtered_data_2020['Matt Kopac'] = pd.to_numeric(filtered_data_2020['Matt Kopac'].str.replace(',', ''), errors='coerce')

# Calculate the total votes per precinct
filtered_data_2020['Total Votes'] = filtered_data_2020['Nida Allam'] + filtered_data_2020['Matt Kopac']

# Calculate the percentage of total votes for each candidate
filtered_data_2020['% Nida Allam'] = (filtered_data_2020['Nida Allam'] / filtered_data_2020['Total Votes']) * 100
filtered_data_2020['% Matt Kopac'] = (filtered_data_2020['Matt Kopac'] / filtered_data_2020['Total Votes']) * 100

# Calculate the difference in percentage points between Nida Allam and Matt Kopac
filtered_data_2020['Indy_estimate_3'] = filtered_data_2020['% Nida Allam'] - filtered_data_2020['% Matt Kopac']

# Display the results
estimate_3 = filtered_data_2020[['Precinct', '% Nida Allam', '% Matt Kopac', 'Indy_estimate_3']]

### Esimate 4

import pandas as pd

# Load the 2020 Commission data
file_path_2020 = '/Users/karthikbalasubramanian/Downloads/2020_Commission.csv'
data_2020 = pd.read_csv(file_path_2020)

# Ensure precinct numbers are in a two-digit format
data_2020['Precinct'] = data_2020['Precinct'].apply(lambda x: str(x).zfill(2))

# Specified precincts, ensuring strings to match potential formatting in the dataset
specified_precincts = [
    "01", "02", "03", "04", "05", "06", "07", "08", "09", "10",
    "14", "15", "17", "18", "19", "20", "21", "22", "23", "24",
    "25", "26", "28", "29", "30-2", "30-3", "32", "36", "37", "40",
    "43", "44", "45", "46", "50", "52"
]

# Filter the data for the specified precincts
filtered_data_2020 = data_2020[data_2020['Precinct'].isin(specified_precincts)]

# Convert vote counts to numeric values for Brenda Howerton and John Rooks, Jr.
filtered_data_2020['Brenda Howerton'] = pd.to_numeric(filtered_data_2020['Brenda Howerton'].str.replace(',', ''), errors='coerce')
filtered_data_2020['John Rooks, Jr.'] = pd.to_numeric(filtered_data_2020['John Rooks, Jr.'].str.replace(',', ''), errors='coerce')

# Calculate the total votes per precinct
filtered_data_2020['Total Votes'] = filtered_data_2020['Brenda Howerton'] + filtered_data_2020['John Rooks, Jr.']

# Calculate the percentage of total votes for each candidate
filtered_data_2020['% Brenda Howerton'] = (filtered_data_2020['Brenda Howerton'] / filtered_data_2020['Total Votes']) * 100
filtered_data_2020['% John Rooks, Jr.'] = (filtered_data_2020['John Rooks, Jr.'] / filtered_data_2020['Total Votes']) * 100

# Calculate the difference in percentage points between Brenda Howerton and John Rooks, Jr.
filtered_data_2020['Indy_estimate_4'] = filtered_data_2020['% Brenda Howerton'] - filtered_data_2020['% John Rooks, Jr.']

# Display the results
estimate_4 = filtered_data_2020[['Precinct', '% Brenda Howerton', '% John Rooks, Jr.', 'Indy_estimate_4']]

### estimate_5 regression

import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import statsmodels.api as sm

# Load the data
file_path = "~/Downloads/Merged_Results_Precinct_Demographics_updated.csv"
data = pd.read_csv(file_path)

# Convert Vote_% from string to numeric
data['Vote_%'] = data['Vote_%'].str.rstrip('%').astype('float') / 100.0

# Drop rows with any missing values
data_clean = data.dropna()

# One-hot encode 'candidate_age' and 'candidate_race' variables
encoder = OneHotEncoder(drop='first')
encoded_vars = encoder.fit_transform(data_clean[['candidate_age', 'candidate_race']]).toarray()
encoded_vars_df = pd.DataFrame(encoded_vars, columns=encoder.get_feature_names_out(['candidate_age', 'candidate_race']), index=data_clean.index)

# Merge the encoded variables back into the dataframe
data_preprocessed = pd.concat([data_clean, encoded_vars_df], axis=1)

# Assuming 'data_preprocessed' is your DataFrame and it already includes binary indicators for candidate race
data_preprocessed['white_alignment'] = data_preprocessed['precinct_%White'] * data_preprocessed['candidate_race_white']
data_preprocessed['black_alignment'] = data_preprocessed['precinct_%Black'] * (1 - data_preprocessed['candidate_race_white'])  # Assuming 1 - candidate_race_white might indicate black or other, adjust according to your data
data_preprocessed['other_alignment'] = data_preprocessed['precinct_%Other'] * (1 - data_preprocessed['candidate_race_white'])  # Adjust this according to your actual variables for race

# Assuming 'data_preprocessed' is your DataFrame and it already includes binary indicators for candidate age
data_preprocessed['young_alignment'] = data_preprocessed['precinct_%Young'] * data_preprocessed['candidate_age_young']
data_preprocessed['old_alignment'] = data_preprocessed['precinct_% Old'] * data_preprocessed['candidate_age_old']

# Drop the original 'candidate_age', 'candidate_race', and 'candidate_sex' columns
data_preprocessed['male'] = np.where(data_preprocessed['candidate_sex'] == 'male', 1, 0)
data_preprocessed.drop(['candidate_age', 'candidate_race', 'candidate_sex', 'Precinct', 'Candidate', 'year'], axis=1, inplace=True)


# Define the independent variables (features) and the dependent variable (target)
X = data_preprocessed.drop(['Vote_%', 'precinct_%Black', 'precinct_%White', 'precinct_%Other', 'precinct_%Young', 'precinct_%Middle', 'precinct_% Old'], axis=1)
y = data_preprocessed['Vote_%']

# Adding a constant to the model for the intercept
X_const = sm.add_constant(X)

# Fit the linear regression model
model = sm.OLS(y, X_const).fit()

# Print the summary of the model
print(model.summary())
