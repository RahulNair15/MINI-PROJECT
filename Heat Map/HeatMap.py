import streamlit as st
import folium
from streamlit_folium import folium_static

# Streamlit app title
st.title("Garbage Heatmap")

garbage_data = [
    {"lat": 19.24260168397352, "lon": 72.85320203456234, "tension_factor": 0.8},
    {"lat": 19.24381721140674, "lon": 72.8571502462596, "tension_factor": 0.6},
    {"lat": 19.247205446695535, "lon": 72.85124301935589, "tension_factor": 0.4},
    {"lat": 19.252877671887852, "lon": 72.84695148490235, "tension_factor": 0.9},
    {"lat": 19.257739423097867, "lon": 72.8556203844985, "tension_factor": 0.7},
    {"lat": 19.252148396777663, "lon": 72.85768032103618, "tension_factor": 1.0},
    {"lat": 19.24876016297229, "lon": 72.86258854893989, "tension_factor": 0.5},
    {"lat": 19.0621, "lon": 72.8777, "tension_factor": 0.8},
    {"lat": 19.0491, "lon": 72.8312, "tension_factor": 0.6},
    {"lat": 19.0173, "lon": 72.8435, "tension_factor": 0.4},
    {"lat": 19.0718, "lon": 72.8233, "tension_factor": 0.9},
    {"lat": 19.0253, "lon": 72.8449, "tension_factor": 0.7},
    {"lat": 19.0844, "lon": 72.8894, "tension_factor": 1.0},
    # {"lat": 18.9960, "lon": 72.8259, "tension_factor": 0.5},
    {"lat": 19.0665, "lon": 72.8606, "tension_factor": 0.8},
    {"lat": 19.0308, "lon": 72.8745, "tension_factor": 0.6},
    {"lat": 19.0456, "lon": 72.8204, "tension_factor": 0.4},
    {"lat": 19.0623, "lon": 72.9284, "tension_factor": 0.9},
    {"lat": 19.0147, "lon": 72.8512, "tension_factor": 0.7},
    {"lat": 19.0782, "lon": 72.9077, "tension_factor": 1.0},
    # {"lat": 18.9707, "lon": 72.8051, "tension_factor": 0.5},
    {"lat": 19.0269, "lon": 72.8645, "tension_factor": 0.8},
    {"lat": 19.0431, "lon": 72.8042, "tension_factor": 0.6},
    {"lat": 19.0582, "lon": 72.8135, "tension_factor": 0.4},
    {"lat": 19.1003, "lon": 72.8822, "tension_factor": 0.9},
    {"lat": 19.1239, "lon": 72.8936, "tension_factor": 0.7},
    {"lat": 19.0982, "lon": 72.9157, "tension_factor": 1.0},
    {"lat": 19.0426, "lon": 72.8677, "tension_factor": 0.5},
    {"lat": 18.9953, "lon": 72.8372, "tension_factor": 0.8},
    {"lat": 19.0358, "lon": 72.8507, "tension_factor": 0.6},
    {"lat": 19.0726, "lon": 72.8180, "tension_factor": 0.4}
]



# Create a Folium map
m = folium.Map(location=[19.25, 72.85], zoom_start=13)

# Generate heatmap data as a list of [lat, lon, tension_factor] for each location
heatmap_data = [[location["lat"], location["lon"], location["tension_factor"]] for location in garbage_data]

# Create a HeatMap layer with the heatmap data
folium.plugins.HeatMap(heatmap_data, min_opacity=0.2, max_val=1.0, radius=15, blur=10, max_zoom=13).add_to(m)

# Display the map using st_folium
folium_static(m)
