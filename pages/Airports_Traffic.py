import streamlit as st
import pandas as pd
import pydeck as pdk

# Import data
try:
    df = pd.read_csv('world_airports.csv')
except FileNotFoundError:
    st.error("Fichier 'world_airports.csv' non trouvé.")
    st.stop()

# Conversion des passagers en float
df["Passengers_float"] = df["Number_of_Passengers"].str.replace("M", "").str.replace(",", "").astype(float)

st.title("🌍 Top 50 Aéroports en 2025 - Carte interactive")

# === Filtre Classement ===
rank_options = {
    "Top 10": 10,
    "Top 20": 20,
    "Top 30": 30,
    "Top 40": 40,
    "Top 50": 50
}
selected_rank = st.selectbox("🏆 Classement", options=list(rank_options.keys()))

# === Application du filtre ===
filtered = df.copy()
max_rank = rank_options[selected_rank]
filtered = filtered[filtered["Rank"] <= max_rank]

# === Gestion des cas où il n'y a pas de données ===
if filtered.empty:
    st.warning("No airport matches the selected criterion.")
else:
    # Calcul du centre de la carte
    lat_mean = filtered["Latitude"].mean() if not filtered["Latitude"].empty else 0
    lon_mean = filtered["Longitude"].mean() if not filtered["Longitude"].empty else 0

    # === Carte avec Pydeck ===
    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=lat_mean,
            longitude=lon_mean,
            zoom=1.5,
            pitch=0,
        ),
        layers=[
            pdk.Layer(
                "ScatterplotLayer",
                data=filtered,
                get_position='[Longitude, Latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius='Passengers_float * 3000',  # Taille proportionnelle au trafic
                pickable=True
            )
        ],
        tooltip={
            "html": "<b>{Name}</b><br>City: {City}<br>Passengers: {Number_of_Passengers}<br>Country: {Country}<br>Rank: {Rank}"
        }
    ))

    # Afficher le nombre d'aéroports trouvés
    st.write(f"Nombre d'aéroports affichés : {len(filtered)}")