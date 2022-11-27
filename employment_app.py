import streamlit as st
import pandas as pd
import altair as alt
import folium
from streamlit_folium import st_folium

st.header("Employment Map")
df = pd.read_csv('data/employment.csv')
df.rename(columns={df.columns[0]:'index'}, inplace=True)
df = df.round({'average': 2})
if st.checkbox("Show Employment Data"):
    st.write(df)


map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron')
choropleth = folium.Choropleth(
    geo_data='us-state-boundaries.geojson',
    data=df,
    columns=('state', 'average'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True,
)
choropleth.geojson.add_to(map)
df = df.set_index('state')
for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['name']

    feature['properties']['employment'] = 'employment rate: ' + str(df.loc[state_name, 'average'] 
                                                                    if state_name in list(df.index) else 'N/A')

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','employment' ], labels=False))
    
st.subheader("Average Employment Rates for all States from 2010-2021")
st_map = st_folium(map, width=700, height=450)

