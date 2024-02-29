import plotly.graph_objects as go
import pandas as pd

# Create pivot table

crosstab = pd.crosstab(sd22_df['vtd_desc'], sd22_df['Universe'], margins=True, margins_name="Total")

# Convert the crosstab to LaTeX
latex_table = crosstab.to_latex()

# Print LaTeX formatted table
print(table.to_latex())


# Your data
data = {
    'A': [218, 1148, 1037, 763, 768, 2197],
    'B': [4111, 5486, 3791, 2412, 2407, 5424],
    'C': [1443, 7994, 8346, 6794, 7048, 12390],
    'D': [3875, 11944, 7712, 5263, 4624, 5514],
    'E': [3252, 3572, 1950, 1051, 823, 695]
}
age_groups = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']

# Convert data to DataFrame and sort it
df = pd.DataFrame(data, index=age_groups)
df_sorted = df.sort_values(by=age_groups, axis=1)

# Define colors for each brand
colors = {'A': 'blue', 'B': 'green', 'C': 'red', 'D': 'yellow', 'E': 'purple'}

# Create the figure
fig = go.Figure()

# Add a trace for each brand
for brand in df_sorted.columns:
    fig.add_trace(go.Bar(
        x=df_sorted.index,
        y=df_sorted[brand],
        name=brand,
        marker_color=colors[brand],  # Use the color defined for this brand
        text=[f'{val}: {brand}' for val in df_sorted[brand]]
    ))

# Update layout
fig.update_layout(barmode='stack')

# Save the figure to a PNG
fig.write_image('/Users/karthikbalasubramanian/Downloads/SD-22/mekko.png')
