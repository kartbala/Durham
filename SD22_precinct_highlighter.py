import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

# Load the GeoJSON file
geojson_path = '/Users/karthikbalasubramanian/Downloads/Voting_Precincts.geojson'
precincts_data = gpd.read_file(geojson_path)

# Normalize 'PRECINCT' values by removing leading zeros for comparison purposes
precincts_data['PRECINCT_norm'] = precincts_data['PRECINCT'].apply(lambda x: x.lstrip('0') if x.isdigit() else x)

# List of specified precincts
specified_precincts = [
    "30-2", "5", "43", "23", "44", "37", "32", "22", "30-1", "45", "2", "50",
    "29", "17", "24", "52", "46", "3", "19", "8", "36", "7", "28", "25", "10",
    "9", "18", "40", "14", "20", "6", "21", "4", "15", "1", "26"
]

# Filter the GeoDataFrame to include only the specified precincts, considering normalized 'PRECINCT' values
sd22 = precincts_data[precincts_data['PRECINCT_norm'].isin(specified_precincts)]

for precinct in specified_precincts:
    try:
        # Create a new figure for each precinct
        fig, ax = plt.subplots(figsize=(10, 20))  # Adjust the size as needed
        
        # Plot all specified precincts in a neutral color
        sd22.plot(ax=ax, edgecolor='black', linewidth=0.5, facecolor='lightgrey')
        
        # Highlight the current precinct in a distinct color
        highlighted = sd22[sd22['PRECINCT_norm'] == precinct]
        if highlighted.empty:
            raise ValueError(f"No data for precinct {precinct}. Skipping...")
        highlighted.plot(ax=ax, edgecolor='black', linewidth=0.5, facecolor='#FFA07A')

        # Add labels to all precincts
        for idx, row in sd22.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['PRECINCT_norm'], (centroid.x, centroid.y), fontsize=10, ha='center', va='center')

        # Set title and remove axes for a cleaner look
        ax.set_title(f"SD-22 with Precinct {precinct} Highlighted", fontsize=15)
        ax.axis('off')

        # Save the plot as a PDF for the current highlighted precinct
        pdf_path = f'/Users/karthikbalasubramanian/Downloads/SD-22/Maps/Highlighted_Precinct_{precinct}.pdf'
        with PdfPages(pdf_path) as pdf:
            pdf.savefig(fig, bbox_inches='tight')
        
        plt.close(fig)  # Close the figure to free memory
    except Exception as e:
        print(f"An error occurred with precinct {precinct}: {e}")
        plt.close(fig)  # Ensure the figure is closed even if an error occurs
