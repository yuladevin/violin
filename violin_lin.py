import pandas as pd
import plotly.graph_objects as go
import os

# Load the data from the provided CSV file
file_path = 'tables/Lin_data.xlsx - Sheet1.csv'
df = pd.read_csv(file_path)

# Extract data columns and species names
data_columns = df.columns[1:]  # Assuming columns B to Y are the data columns
species_names = df['species'].unique()

# Create directory to save the plots
output_dir = 'Lin'
os.makedirs(output_dir, exist_ok=True)

# Create a subplot for each metal and save each plot separately
for metal in data_columns:
    fig = go.Figure()
    
    for species in species_names:
        species_data = df[df['species'] == species]
        metal_data = species_data[metal].dropna()  # Exclude NaN values

        if not metal_data.empty:
            fig.add_trace(go.Violin(
                y=metal_data,
                name=species,
                box_visible=True,
                meanline_visible=True
            ))

    # Update layout
    fig.update_layout(
        title=f"Distribution of {metal} Concentrations for Each Species",
        yaxis_title="Concentration",
        xaxis_title="Species",
        showlegend=False
    )

    # Save the figure
    output_path = os.path.join(output_dir, f"{metal}_concentration_distribution.png")
    fig.write_image(output_path)

print("Plots saved successfully.")
