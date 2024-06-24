import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Function to generate violin plots and display them
def generate_plots(df, color_map):
    data_columns = df.columns[1:]  # Assuming columns B to Y are the data columns
    species_names = df['species'].unique()

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
                    meanline_visible=True,
                    line_color=color_map.get(species, 'black'),  # Apply color from the color map
                    fillcolor=color_map.get(species, 'black')  # Apply fill color from the color map
                ))

        # Update layout
        fig.update_layout(
            title=f"Distribution of {metal} Concentrations for Each Species",
            yaxis_title="Concentration",
            xaxis_title="Species",
            showlegend=True
        )

        # Display the figure in Streamlit
        st.plotly_chart(fig)

# Streamlit interface
st.title("Metal Concentration Distribution")

st.write("""
Upload a CSV file with your data and generate violin plots for each metal's concentration across different species.
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data preview:", df.head())
    
    species_names = df['species'].unique()
    color_map = {}

    st.write("Select colors for each species:")
    for species in species_names:
        color = st.color_picker(f"Pick a color for {species}", "#000000")
        color_map[species] = color

    generate_plots(df, color_map)
