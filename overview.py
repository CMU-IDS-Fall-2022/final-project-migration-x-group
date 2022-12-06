from data_munging import ALL_STATES_TITLE
import pandas as pd
import numpy as np
import streamlit as st
import plot_migration
from logzero import logger
import streamlit as st
import altair as alt
from re import U
import seaborn as sns

import folium
from streamlit_folium import st_folium #interface between strealit and folium

def show_state_by_state_migration():
    

    ######### VIZ 1 - OVERVIEW MAP #########

    #Read state migration data
    state_migration_df = pd.read_csv("data/state_migration.csv")

    # Selection box for overview map
    origin_state = st.selectbox(
        'Select origin state',
        (state_migration_df["o_state_name"].unique()))

    #Filter data for selected origin state 
    filt = state_migration_df["o_state_name"] == origin_state
    state_migration_filtered_df = state_migration_df[filt]

    # Calculate and add percentages of total adults from selected origin to dataframe 
    total_people = state_migration_filtered_df['n'].sum()
    state_migration_filtered_df["perc_of_total"] = round((state_migration_filtered_df["n"] / total_people) * 100, 2)


    #Filter for where state and origin are the same.
    filt = state_migration_filtered_df["o_state_name"] == state_migration_filtered_df["d_state_name"]

    #Grab the number of people who stated
    people_who_stayed = int(state_migration_filtered_df[filt]["n"])

    # Drop where origin and destination is the same. Exclude the origin state 
    state_migration_filtered_df = state_migration_filtered_df.drop(index=state_migration_filtered_df[filt].index)

    #Specify overview map 
    #Folium library quickstart https://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
    map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron') #Creating Folium MNap

    choropleth = folium.Choropleth(
        geo_data='data/us-state-boundaries.geojson',
        data=state_migration_filtered_df,
        columns=("d_state_name", "n"),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    #Set destination state as index
    state_migration_filtered_df = state_migration_filtered_df.set_index('d_state_name')
    #Add needed data to geojson
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['migrants'] = 'migrants: ' + str(state_migration_filtered_df.loc[state_name, 'n'] 
                                if state_name in list(state_migration_filtered_df.index) else 'N/A')
        feature['properties']['perc_of_total'] = 'perc_of_total: ' + str(state_migration_filtered_df.loc[state_name, 'perc_of_total'] 
                                if state_name in list(state_migration_filtered_df.index) else 'N/A')
        #TODO: Add features from the dataframe to geojson file
        #feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
        #feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name','migrants', 'perc_of_total' ], labels=False),
    )

    #Specify columns for metrics and viz
    cols = st.columns(2)
    with cols[0]:
        #Display overview map
        st_map = st_folium(map, width=720, height=450) 

    with cols[1]:
        st.metric(label="Total adults from {}".format(origin_state), value=total_people)
        st.metric(label="Percent of adults that stayed in {}".format(origin_state), value='{:.2%}'.format((people_who_stayed / total_people)))
    #Show migration table if checked
    state_migration_bar = alt.Chart(state_migration_filtered_df.reset_index()).mark_bar().encode(
        alt.Y("n", type="quantitative", title="migrant_count"),
        alt.X(field='d_state_name', type='nominal', sort='-y'),
    ).properties(
        title="Count of Migranted Adults from {} by Destination State".format(origin_state)
    )
    st.write(state_migration_bar)
            
    if st.checkbox("Show Migration table"):   
        st.write(state_migration_filtered_df)
            

    #TODO: Maube use this as a filter for something else...Possibly used
    state_name = ''
    if st_map['last_active_drawing']:
        state_name = st_map['last_active_drawing']['properties']['name']

    #TODO: Insert Bar Chart of Destinations from selected State
    #st.bar_chart(state_lvl_migr)

def show_inbound_map():

    state_lvl_migr_df = pd.read_csv("data/state_migration_summary_with_rate.csv")
    #Specify overview map 
    #Folium library quickstart https://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
    map = folium.Map(location=[38, -96.5], zoom_start=3, scrollWheelZoom=False, tiles='CartoDB positron') #Creating Folium MNap
    
    choropleth = folium.Choropleth(
        geo_data='data/us-state-boundaries.geojson',
        data=state_lvl_migr_df,
        columns=("state", "inbound_rate"),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    #Set destination state as index
    state_lvl_migr_df = state_lvl_migr_df.set_index('state')
    #Add needed data to geojson
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['inbound_rate'] = 'inbound_rate: ' + str(state_lvl_migr_df.loc[state_name, 'inbound_rate'] 
                                if state_name in list(state_lvl_migr_df.index) else 'N/A')
        #TODO: Add features from the dataframe to geojson file
        #feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
        #feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name','inbound_rate'], labels=False),
    )
    st_map = st_folium(map, width=720, height=450) 


def show_outbound_map():

    state_lvl_migr_df = pd.read_csv("data/state_migration_summary_with_rate.csv")
    #Specify overview map 
    #Folium library quickstart https://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
    map = folium.Map(location=[38, -96.5], zoom_start=3, scrollWheelZoom=False, tiles='CartoDB positron') #Creating Folium MNap
    
    choropleth = folium.Choropleth(
        geo_data='data/us-state-boundaries.geojson',
        data=state_lvl_migr_df,
        columns=("state", "outbound_rate"),
        key_on='feature.properties.name',
        line_opacity=0.8,
        highlight=True
    )
    choropleth.geojson.add_to(map)

    #Set destination state as index
    state_lvl_migr_df = state_lvl_migr_df.set_index('state')
    #Add needed data to geojson
    for feature in choropleth.geojson.data['features']:
        state_name = feature['properties']['name']
        feature['properties']['outbound_rate'] = 'outbound_rate: ' + str(state_lvl_migr_df.loc[state_name, 'outbound_rate'] 
                                if state_name in list(state_lvl_migr_df.index) else 'N/A')
        #TODO: Add features from the dataframe to geojson file
        #feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
        #feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(['name','outbound_rate'], labels=False),
    )
    st_map = st_folium(map, width=720, height=450) 

def show_inbound_vs_outbound_maps():
    
    st.markdown(
        """
        The purpose of this section is to which states have had the highest inflow and outflow of young adults.
        We calculate the inbound and outbound rates as follows:
        -  `inbound_rate = (adults_migrated to state) / total of adults from state`
        -  `outbound_rate = (adults_migrated from state) / total of adults from state`
        """
    )
    state_lvl_migr = pd.read_csv("data/state_migration_summary_with_rate.csv")

    if st.checkbox("Show Raw Outbound and Inbound Data"):
        st.write(state_lvl_migr)

    cols = st.columns(2)
    with cols[0]:
        st.markdown("#### States outbound migration rate")
        show_outbound_map()
        st.markdown(
            """
            Colarado, Nevada, and DC have the highest rate of *departing* young adults moving *from* the states.  Their young adult populations decreased by larger rates than other states.
            """
        )
        #outbound bar
        
    with cols[1]:
        st.markdown("#### States inbound migration") 
        show_inbound_map()

        st.markdown(
            """
            New Hampshire, Vermont, and Wyoming have the highest rate of *incoming* young adults moving *into* the states. Their young adult populations increased by larger rates than other states.
            """
        )   
    
    # Bar charts showing inpund and outbound

    outbound_bar = alt.Chart(state_lvl_migr.reset_index()).mark_bar().encode(
    alt.Y("outbound_rate", type="quantitative", title="outbound rate"),
    alt.X(field='state', type='nominal', sort='-y'),
    ).properties(
        title="Outbound rate of states"
    )
    st.write(outbound_bar)

    inbound_bar = alt.Chart(state_lvl_migr.reset_index()).mark_bar().encode(
        alt.Y("inbound_rate", type="quantitative", title="inbound rate"),
        alt.X(field='state', type='nominal', sort='-y'),
        ).properties(
            title="Inbound rate of states"
        )
    st.write(inbound_bar)

    

    #st.write((state_lvl_migr.nlargest(5, columns="inbound_rate")["state"]))
