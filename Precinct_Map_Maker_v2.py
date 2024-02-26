import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx

# Load the GeoJSON file for precincts
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# List of specified precincts with single-digit numbers not padded with a leading zero
specified_precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Ensure data is in Web Mercator (EPSG:3857) for compatibility with contextily
precincts_data = precincts_data.to_crs(epsg=3857)

# Iterate over the list of specified precincts
for precinct in specified_precincts:
    # Filter the GeoDataFrame for the current precinct, considering both '6' and '06' formats
    precinct_data = precincts_data[precincts_data['PRECINCT'].isin([precinct, precinct.zfill(2)])]

    # Check if there is any data for the current precinct
    if not precinct_data.empty:
        # Plotting the map for the current precinct
        fig, ax = plt.subplots(figsize=(36, 48))  # Set figure size to 36" x 48"

        # Plot the current precinct
        precinct_data.plot(ax=ax, edgecolor='black', linewidth=4, facecolor='none')

        # Add OpenStreetMap as base layer
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

        # Customizations
        ax.set_title(f"Map for Precinct {precinct} with OpenStreetMap Base", fontsize=20)
        ax.set_axis_off()

        # Adjust the view to the extent of your data
        ax.set_xlim(precinct_data.total_bounds[[0, 2]])
        ax.set_ylim(precinct_data.total_bounds[[1, 3]])

        plt.show()

        # Save the plot to a PDF
        pdf_path = f'/Users/karthikbalasubramanian/Downloads/SD-22/Maps/Precinct_{precinct}_Map_with_OSM_Base.pdf'
        fig.savefig(pdf_path, bbox_inches='tight')

        print(f"Map for Precinct {precinct} with OpenStreetMap base saved to {pdf_path}")
    else:
        print(f"No data found for Precinct {precinct}.")

#### Rename maps to deal with padded 0

import glob
import os
import re

# Directory where the files are located
directory = '/Users/karthikbalasubramanian/Downloads/SD-22/Maps'

# Pattern to match files of interest
pattern = 'Precinct_*_Map_with_Points.pdf'

# Full path pattern
full_path_pattern = os.path.join(directory, pattern)

# Function to add leading zero to single digit precinct numbers in filenames
def format_precinct_number(filename):
    # Regular expression to find the precinct number part in the filename
    new_name = re.sub(r'Precinct_([0-9]{1})_Map_with_Points\.pdf', r'Precinct_0\1_Map_with_Points.pdf', filename)
    return new_name

# Find all files in the directory that match the pattern
for filepath in glob.glob(full_path_pattern):
    # Extract the filename from the full path
    filename = os.path.basename(filepath)
    
    # Format the precinct number in the filename
    new_filename = format_precinct_number(filename)
    
    # Only rename the file if the filename has changed
    if new_filename != filename:
        # Construct the full path for the new filename
        new_filepath = os.path.join(directory, new_filename)
        
        # Rename the file
        os.rename(filepath, new_filepath)
        
        print(f'Renamed "{filename}" to "{new_filename}"')
 
### Getting voter geotagged data

import os

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file matches the pattern and has a double extension
    if filename.startswith("Precinct_") and filename.endswith(".gpkg.gpkg"):
        # Remove the redundant ".gpkg" extension
        new_filename = filename.replace(".gpkg.gpkg", ".gpkg")
        
        # Split the filename to separate the precinct number and any additional identifier
        parts = new_filename.replace("Precinct_", "").replace(".gpkg", "").split("_")
        precinct_number = parts[0]
        additional_identifier = '_'.join(parts[1:])  # Join back any remaining parts as the identifier
        
        # Pad the precinct number with a zero if it's a single digit
        if precinct_number.isdigit() and len(precinct_number) == 1:
            precinct_number = f"0{precinct_number}"
        
        # Reconstruct the new filename with corrections
        new_filename = f"Precinct_{precinct_number}"
        if additional_identifier:
            new_filename += f"_{additional_identifier}"
        new_filename += ".gpkg"

        # Construct the full old and new file paths
        old_file_path = os.path.join(directory, filename)
        new_file_path = os.path.join(directory, new_filename)

        # Rename the file
        os.rename(old_file_path, new_file_path)
        print(f"Renamed '{filename}' to '{new_filename}'")

### Add voters

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as ctx
from matplotlib.lines import Line2D
from matplotlib.offsetbox import OffsetImage, AnnotationBbox

# Load the GeoJSON file for precincts
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# Convert precincts_data to the same CRS (Web Mercator) for compatibility with contextily
precincts_data = precincts_data.to_crs(epsg=3857)

# List of specified precincts with single-digit numbers not padded with a leading zero
specified_precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Define colors for each 'Universe' category
color_map = {'A': 'red', 'B': 'green', 'C': 'blue'}

# Base path for points data files
points_base_path = '/Users/karthikbalasubramanian/Downloads/SD-22/Maps/Precinct_{}.gpkg'

# Loop through each specified precinct
for precinct_number in specified_precincts:
    # Format the precinct number to match the file naming convention
    formatted_precinct_number = precinct_number.replace('-', '_')
    points_path = points_base_path.format(formatted_precinct_number.zfill(2))  # Ensure two-digit format

    # Load the points data for the current precinct
    try:
        points_data = gpd.read_file(points_path)
    except FileNotFoundError:
        print(f"Points data file not found for Precinct {precinct_number}. Skipping...")
        continue

    # Convert points_data to the same CRS (Web Mercator)
    points_data = points_data.to_crs(epsg=3857)

    # Filter precincts_data for the current precinct
    precinct_data = precincts_data[precincts_data['PRECINCT'].isin([precinct_number, precinct_number.zfill(2)])]

    if not precinct_data.empty:
        # Clip the points data to the precinct boundary
        points_within_precinct = gpd.clip(points_data, precinct_data)

        # Filter out points that do not belong to 'A', 'B', or 'C' categories
        points_within_precinct = points_within_precinct[points_within_precinct['Universe'].isin(color_map.keys())]

        # Update the 'color' column after filtering
        points_within_precinct['color'] = points_within_precinct['Universe'].map(color_map)

        # Plotting
        fig, ax = plt.subplots(figsize=(36, 48))  # Large figure size as specified

        # Plot the precinct boundary
        precinct_data.plot(ax=ax, edgecolor='black', linewidth=2, facecolor='none')

        # Plot the points within the precinct with colors based on 'Universe'
        for color, df in points_within_precinct.groupby('color'):
            df.plot(ax=ax, marker='o', color=color, markersize=30, label=color)

        # Add OpenStreetMap as base layer
        ctx.add_basemap(ax, source=ctx.providers.OpenStreetMap.Mapnik)

        # Customizations
        ax.set_title(f"Map for Precinct {precinct_number} with Points", fontsize=20)
        ax.set_axis_off()

        # Legend
        legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=15, label=label)
                           for label, color in color_map.items()]
        ax.legend(handles=legend_elements, title='Universe')

        # Add the logo to the very top left corner
        logo_path = '/Users/karthikbalasubramanian/Downloads/Sophia-For-NC-Senate-LOGO.png'
        logo = plt.imread(logo_path)
        imagebox = OffsetImage(logo, zoom=0.05)  # Reduced zoom for a smaller logo
        ab = AnnotationBbox(imagebox, (0, 1), xycoords='axes fraction', boxcoords="axes fraction", box_alignment=(0, 1), frameon=False)
        ax.add_artist(ab)

        # Save the plot to a file
        pdf_path = f'/Users/karthikbalasubramanian/Downloads/SD-22/Maps/Precinct_{formatted_precinct_number}_Map_with_Points.pdf'
        fig.savefig(pdf_path, bbox_inches='tight', dpi=300)  # Increase the DPI for better resolution

        print(f"Map for Precinct {precinct_number} with points saved to {pdf_path}")
        plt.close(fig)  # Close the figure to free memory
    else:
        print(f"No precinct boundary data found for Precinct {precinct_number}.")
