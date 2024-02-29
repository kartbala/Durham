# * Imports

# Importing pandas
import pandas as pd
import os
from fuzzywuzzy import fuzz
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

# Define file paths for Excel files with the provided path
sd22_df = pd.read_csv('~/Downloads/SD-22/sd22_targeting.csv', dtype={'full_phone_number': str})

# Define age bins and labels excluding under 18
age_bins = [18, 25, 35, 45, 55, 65, float('inf')]  # Starting from 18
age_labels = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']

# Categorize each age into one of the bins
sd22_df['Age_Group'] = pd.cut(sd22_df['age_at_year_end'], bins=age_bins, labels=age_labels, right=False)

# 'right=False' means the intervals are including the left endpoint and excluding the right endpoint.


import pandas as pd
import plotly.express as px

# Sample data
data = {'Universe': ['A','B','C','D','E'],
        '18-24': [10, 20, 15, 5, 8],
        '25-34': [15, 10, 20, 10, 12],
        '35-44': [20, 15, 10, 15, 20],
        '45-54': [5, 12, 8, 10, 15],
        '55+': [8, 10, 12, 15, 10]}

df = pd.DataFrame(data)

# Melt dataframe  
df = df.melt(id_vars='Universe', 
             var_name='AgeGroup',
             value_name='Value')

# Sort by universe and value            
df = df.sort_values(['Universe', 'Value'], ascending=[True, False])

# Plot 
fig = px.bar(df, x='Universe', y='Value', color='AgeGroup',
             orientation='h', barmode='stack')

fig.update_layout(
     title='Audience by Age Group',
     yaxis_title='Age Group',
     xaxis_title='Value'
)

fig.show()

sd22_df 'Age_Group' and 'Universe'
