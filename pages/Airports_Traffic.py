import streamlit as st
import pandas as pd
import pydeck as pdk

# Import data
df = pd.read_csv('world_airports.csv')

# Conversion des passagers en float
df["Passengers_float"] = df["Number_of_Passengers"].str.replace("M", "").str.replace(",", "").astype(float)

st.title("🌍 Top 50 Aéroports en 2025 - Carte interactive")

# === Filtres ===
countries = sorted(df["Country"].unique())
selected_country = st.selectbox("🌐 Sélectionner un pays", options=["All"] + countries)

traffic_options = {
    "< 50M": (0, 50),
    "50M – 75M": (50, 75),
    "75M – 100M": (75, 100),
    "> 100M": (100, float("inf"))
}
selected_traffic = st.selectbox("✈️ Trafic passagers", options=list(traffic_options.keys()))

rank_options = {
    "Top 10": 10,
    "Top 20": 20,
    "Top 30": 30,
    "Top 40": 40,
    "Top 50": 50
}
selected_rank = st.selectbox("🏆 Classement", options=list(rank_options.keys()))

# === Application des filtres ===
min_pax, max_pax = traffic_options[selected_traffic]
max_rank = rank_options[selected_rank]

filtered = df[df["Passengers_float"].between(min_pax, max_pax)]
filtered = filtered[filtered["Rank"] <= max_rank]
if selected_country != "All":
    filtered = filtered[filtered["Country"] == selected_country]

# === Carte avec Pydeck ===
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=filtered["Latitude"].mean(),
        longitude=filtered["Longitude"].mean(),
        zoom=1.5,
        pitch=0,
    ),
    layers=[
        pdk.Layer(
            "ScatterplotLayer",
            data=filtered,
            get_position='[Longitude, Latitude]',
            get_color='[200, 30, 0, 160]',
            get_radius=500000,
            pickable=True
        )
    ],
    tooltip={"text": "{Name}\nCity: {City}\nPassengers: {Number_of_Passengers}"}
))