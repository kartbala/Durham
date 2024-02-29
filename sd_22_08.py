import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load the GeoJSON file
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# Normalize 'PRECINCT' values by removing leading zeros for comparison purposes
precincts_data['PRECINCT_norm'] = precincts_data['PRECINCT'].apply(lambda x: x.lstrip('0') if x.isdigit() else x)

# List of specified precincts with single-digit numbers not padded with a leading zero
specified_precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Filter the GeoDataFrame to include only the specified precincts, considering normalized 'PRECINCT' values
sd22 = precincts_data[precincts_data['PRECINCT_norm'].isin(specified_precincts)]

# Save the filtered GeoDataFrame
sd22_path = '/Users/karthikbalasubramanian/Downloads/sd22.geojson'
sd22.to_file(sd22_path, driver='GeoJSON')

# Plotting the filtered map with labels
fig, ax = plt.subplots(figsize=(42, 96))  # Size in inches

# Use a lambda function to apply colors conditionally. Precinct 8 will be colored light orange.
sd22['color'] = sd22['PRECINCT_norm'].apply(lambda x: '#FFA07A' if x == '8' else 'none')  # Light orange for precinct 8

# Plot with conditional coloring
sd22.plot(ax=ax, edgecolor='black', linewidth=1, facecolor=sd22['color'])

# Add labels with a smaller font size
for idx, row in sd22.iterrows():
    # Use the centroid of each polygon for the label location
    centroid = row.geometry.centroid
    label = row['PRECINCT']  # Use the original precinct name for labeling
    ax.annotate(label, (centroid.x, centroid.y), fontsize=20, ha='center', va='center')  # Reduced font size

# Set the new title with a smaller font size
ax.set_title("SD-22 Precinct Map", fontsize=25)

# Adjust axis labels to match the reduced title and label sizes
ax.set_xlabel("Longitude", fontsize=20)
ax.set_ylabel("Latitude", fontsize=20)

# Remove axis for a cleaner look
ax.axis('off')

# Save the plot as a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/SD-22_Precinct_Map_08_2.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path

# filter all the voting records for precinct 08
sd22_08_df = sd22_df[sd22_df['vtd_desc'] == "08"]
sd22_08_df.to_csv('/Users/karthikbalasubramanian/Downloads/SD-22/sd22_08_targeting.csv', index=False)

# polygon for precinct 08
precinct_08_gdf = sd22[sd22['PRECINCT'] == '8']

# Check if precinct "08" data exists
if not precinct_08_gdf.empty:
    # Plotting
    fig, ax = plt.subplots(figsize=(10, 10))  # Adjust the figure size as needed
    precinct_08_gdf.plot(ax=ax, edgecolor='blue', facecolor='none')  # Customize colors as needed

    # Add customization
    ax.set_title('Map for Precinct 08', fontsize=15)
    ax.set_axis_off()  # Hide axis

    plt.show()  # Display the plot

    fig.savefig('/Users/karthikbalasubramanian/Downloads/SD-22/Maps/Precinct_08_Map_2.pdf', bbox_inches='tight')
else:
    print("No data found for Precinct 08.")

# import sd22 08 voter file data
file_path = "/Users/karthikbalasubramanian/Downloads/SD-22/Maps/sd22_08.gpkg"  # Adjusted to the accessible path in this environment

# Load precinct polygons GeoJSON
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# Filter for precinct "08" polygon
precinct_08_polygon = precincts_data[precincts_data['PRECINCT'] == '8']

# Load roads from the GeoPackage
roads_path = '/Users/karthikbalasubramanian/Downloads/Roads (Intersected).gpkg'  # Adjusted to the accessible path in this environment
roads_data = gpd.read_file(roads_path)
roads_within_precinct_08 = gpd.clip(roads_data, precinct_08_polygon)
points_within_precinct_08 = gpd.clip(precinct_08_points, precinct_08_polygon)

# Plotting
fig, ax = plt.subplots(figsize=(10, 10))

# Plot precinct "08" polygon as the base layer
precinct_08_polygon.plot(ax=ax, edgecolor='black', facecolor='none', linewidth=2)

# Plot clipped roads within precinct "08"
roads_within_precinct_08.plot(ax=ax, linewidth=1, color='gray')

# Label some major roads (assuming 'name' column exists in roads data)
for idx, row in roads_within_precinct_08.iterrows():
    if not row.geometry.is_empty:  # Check if the geometry is not empty
        # Get the centroid of the road for labeling
        xy = row.geometry.centroid.coords[0]
        # Use the 'name' column for the road label. Ensure this column exists in your roads data.
        road_name = row.get('name', 'Unnamed Road')  # Default to 'Unnamed Road' if 'name' column is missing
        # Annotate the road name on the plot
        ax.annotate(text=road_name, xy=xy, horizontalalignment='center', fontsize=8, color='darkgrey', clip_on=True)

# Plot clipped voter points within precinct "08" with color based on 'Universe'
colors = points_within_precinct_08['Universe'].map({'A': 'orange', 'B': 'blue'}).fillna('gray')
ax.scatter(points_within_precinct_08.geometry.x, points_within_precinct_08.geometry.y, color=colors, s=10)

# Customizations
ax.set_title('Precinct 08 with Roads and Targeting Data', fontsize=15)
ax.set_axis_off()

# Save the plot to a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/SD-22/Maps/Precinct_08_Map_with_Roads_and_Labels.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

plt.close(fig)  # Close the figure

print(f"Map saved to {pdf_path}")

## Latex table for streets

# Function to extract just the street name from the address
def extract_street_name(address):
    address = address.strip().upper()  # Normalize the address
    street_name = re.sub(r'\b\d+\b', '', address)  # Remove numbers
    street_name = re.sub(r'\s+#.*', '', street_name)  # Remove apartment/unit numbers
    street_name = re.sub(r'\s+\d+.*', '', street_name)  # Remove trailing numbers and suffixes
    street_name = street_name.strip()  # Final cleanup
    return street_name

def generate_latex_table(file_path, output_path):
    # Load the data
    data = pd.read_csv(file_path)

    # Extract street names
    data['street_name'] = data['res_street_address'].apply(extract_street_name)

    # Create a crosstab
    crosstab = pd.crosstab(data['street_name'], data['Universe'])

    # Sort the crosstab by 'A' in descending order
    crosstab_sorted = crosstab.sort_values(by='A', ascending=False)

    # Generate LaTeX code
    latex_code = crosstab_sorted.to_latex()

    # Write the LaTeX code to a file in the specified directory
    with open(output_path, 'w') as file:
        file.write(latex_code)

# Set your file paths
file_path = '/Users/karthikbalasubramanian/Downloads/SD-22/Maps/sd22_08_targeting.csv'
output_path = '/Users/karthikbalasubramanian/Downloads/SD-22/Maps/aggregated_crosstab_sorted.tex'

# Generate the LaTeX table
generate_latex_table(file_path, output_path)

print(f'LaTeX table has been generated at {output_path}')
