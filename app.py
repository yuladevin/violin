import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import os

# Function to generate and save violin plots
def generate_plots(df, output_dir):
    data_columns = df.columns[1:]  # Assuming columns B to Y are the data columns
    species_names = df['species'].unique()

    os.makedirs(output_dir, exist_ok=True)

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
        st.image(output_path)

# Streamlit interface
st.title("Metal Concentration Distribution")

st.write("""
Upload a CSV file with your data and generate violin plots for each metal's concentration across different species.
""")

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Data preview:", df.head())

    output_dir = "plots"
    generate_plots(df, output_dir)
    st.write(f"Plots have been saved in the `{output_dir}` directory and displayed below.")