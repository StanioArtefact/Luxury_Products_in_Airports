import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("Visitors_Spendings.csv")

# Title
st.title("Top 20 Countries by Visitor Expenditure")

# Year selector using dropdown
years = sorted(df['Year'].unique())
year = st.selectbox("Select a year:", years, index=years.index(2022))

# Filter by selected year
filtered_df = df[df['Year'] == year].copy()

# Compute rank
filtered_df = filtered_df.sort_values(by='Expenditure_per_Visitor', ascending=False)
filtered_df['Rank'] = range(1, len(filtered_df) + 1)

# Keep top 20 only
top20 = filtered_df.head(20)

# Plot bar chart
fig = px.bar(
    top20.sort_values('Expenditure_per_Visitor', ascending=True),  # for horizontal bar chart from smallest to largest
    x='Expenditure_per_Visitor',
    y='Country',
    orientation='h',
    text='Expenditure_per_Visitor',
    hover_data={'Country': True, 'Expenditure_per_Visitor': True, 'Rank': True},
    title=f"Top 20 Countries by Visitor Expenditure in {year}"
)
fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')
fig.update_layout(
    xaxis_title="Expenditure per Visitor (USD)",
    yaxis_title="Country",
    yaxis=dict(categoryorder='total ascending'),
    margin=dict(l=100, r=20, t=50, b=50)
)

st.plotly_chart(fig, use_container_width=True)