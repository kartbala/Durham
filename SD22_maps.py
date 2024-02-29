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

# Plot without filling the polygons and with larger borders if desired
sd22.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)

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
pdf_path = '/Users/karthikbalasubramanian/Downloads/SD-22_Precinct_Map.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path


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

# Plot without filling the polygons and with larger borders if desired
sd22.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)

# Add labels with a slightly smaller font size
for idx, row in sd22.iterrows():
    # Use the centroid of each polygon for the label location
    centroid = row.geometry.centroid
    label = row['PRECINCT']  # Use the original precinct name for labeling
    ax.annotate(label, (centroid.x, centroid.y), fontsize=40, ha='center', va='center')

# Add titles and labels if needed
ax.set_title("Filtered Durham County Voting Precincts", fontsize=50)
ax.set_xlabel("Longitude", fontsize=30)
ax.set_ylabel("Latitude", fontsize=30)

# Remove axis for a cleaner look
ax.axis('off')

# Save the plot as a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/Filtered_Durham_County_Voting_Precincts_Map.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load the GeoJSON file
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# List of specified precincts
specified_precincts = [
    "30-2", "05", "43", "23", "44", "37", "32", "22", "30-1", "45", "02", "50",
    "29", "17", "24", "52", "46", "03", "19", "08", "36", "07", "28", "25", "10",
    "09", "18", "40", "14", "20", "06", "21", "04", "15", "01", "26"
]

# Filter the GeoDataFrame to include only the specified precincts
sd22 = precincts_data[precincts_data['PRECINCT'].isin(specified_precincts)]

# Save the filtered GeoDataFrame
sd22_path = '/Users/karthikbalasubramanian/Downloads/sd22.geojson'
sd22.to_file(sd22_path, driver='GeoJSON')

# Plotting the filtered map with labels
fig, ax = plt.subplots(figsize=(42, 96))  # Size in inches

# Plot without filling the polygons and with larger borders if desired
sd22.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)

# Add labels slightly smaller than before
for idx, row in sd22.iterrows():
    # Use the centroid of each polygon for the label location
    centroid = row.geometry.centroid
    label = row['PRECINCT']
    ax.annotate(label, (centroid.x, centroid.y), fontsize=40, ha='center', va='center')  # Slightly smaller font size

# Add titles and labels if needed
ax.set_title("Filtered Durham County Voting Precincts", fontsize=50)
ax.set_xlabel("Longitude", fontsize=30)
ax.set_ylabel("Latitude", fontsize=30)

# Remove axis for a cleaner look
ax.axis('off')

# Save the plot as a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/Filtered_Durham_County_Voting_Precincts_Map.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load the GeoJSON file
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# List of specified precincts
specified_precincts = [
    "30-2", "05", "43", "23", "44", "37", "32", "22", "30-1", "45", "02", "50",
    "29", "17", "24", "52", "46", "03", "19", "08", "36", "07", "28", "25", "10",
    "09", "18", "40", "14", "20", "06", "21", "04", "15", "01", "26"
]

# Filter the GeoDataFrame to include only the specified precincts
sd22 = precincts_data[precincts_data['PRECINCT'].isin(specified_precincts)]

# Save the filtered GeoDataFrame
sd22_path = '/Users/karthikbalasubramanian/Downloads/sd22.geojson'
sd22.to_file(sd22_path, driver='GeoJSON')

# Plotting the filtered map
fig, ax = plt.subplots(figsize=(42, 96))  # Size in inches

# Plot without filling the polygons and with larger borders if desired
sd22.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)

# Add titles and labels if needed
ax.set_title("Filtered Durham County Voting Precincts", fontsize=50)
ax.set_xlabel("Longitude", fontsize=30)
ax.set_ylabel("Latitude", fontsize=30)

# Remove axis for a cleaner look
ax.axis('off')

# Save the plot as a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/Filtered_Durham_County_Voting_Precincts_Map.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load the GeoJSON file
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# Plotting the map
fig, ax = plt.subplots(figsize=(42, 96))  # Size in inches
precincts_data.plot(ax=ax)

# Add titles and labels if needed
ax.set_title("Durham County Voting Precincts")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")

# Save the plot as a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/Durham_County_Voting_Precincts_Map_3.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path
    


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load the GeoJSON file
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# Plotting the map
fig, ax = plt.subplots(figsize=(42, 96))  # Size in inches

# Plot without filling the polygons and with larger borders if desired
precincts_data.plot(ax=ax, facecolor='none', edgecolor='black', linewidth=1)

# Loop through each precinct to add huge labels at their centroids
for idx, row in precincts_data.iterrows():
    # Use the centroid of each polygon for the label location
    centroid = row.geometry.centroid
    label = row['PRECINCT']  # Assuming 'PRECINCT' is the column with precinct labels. Adjust if needed.
    ax.annotate(label, (centroid.x, centroid.y), fontsize=50, ha='center', va='center')

# Add titles and labels if needed
ax.set_title("Durham County Voting Precincts", fontsize=50)
ax.set_xlabel("Longitude", fontsize=30)
ax.set_ylabel("Latitude", fontsize=30)

# Remove axis for a cleaner look
ax.axis('off')

# Save the plot as a PDF
pdf_path = '/Users/karthikbalasubramanian/Downloads/Durham_County_Voting_Precincts_Map_3.pdf'
with PdfPages(pdf_path) as pdf:
    pdf.savefig(fig, bbox_inches='tight')

pdf_path
