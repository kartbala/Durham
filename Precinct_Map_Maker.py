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
pattern = 'Precinct_*_Map_with_OSM_Base.pdf'

# Full path pattern
full_path_pattern = os.path.join(directory, pattern)

# Function to add leading zero to single digit precinct numbers in filenames
def format_precinct_number(filename):
    # Regular expression to find the precinct number part in the filename
    new_name = re.sub(r'Precinct_([0-9]{1})_Map_with_OSM_Base\.pdf', r'Precinct_0\1_Map_with_OSM_Base.pdf', filename)
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

