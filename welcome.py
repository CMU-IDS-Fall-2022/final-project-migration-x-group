import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

import folium
from streamlit_folium import st_folium #interface between strealit and folium

#import team files
import overview
import median_income_process

@st.cache(allow_output_mutation=True)  # add caching so we load the data only once
def load_data(file_path):
    return pd.read_csv(file_path)


padding = 0
st.set_page_config(page_title="Young Adult Migration and Its Social-Economic Impacts", layout="wide", page_icon="📍")

st.markdown(
    """
    <style>
    .small-font {
        font-size:12px;
        font-style: italic;
        color: #b1a7a6;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.image("img/migration_img.jpeg")


## NEW PROJECT START ##
st.title("U.S. Young Adult Migration Analysis")


# Welcome page


st.markdown("## 1. Overview of Young Adult Migration")
st.write(
    """ 
    Young adults entering the workforce are important to economic development, but some states in the U.S. see more migration of young adults than others, leading to inequities in workforce development. \
    Therefore, we propose an interactive data science application that allows stakeholders in economic development to interpret migration patterns of young adults from their state.
    """
)
uu = "https://www.google.com/url?q=https://data.migrationpatterns.org/MigrationPatternsData.zip&sa=D&source=docs&ust=1670519605674757&usg=AOvVaw2DKNPWFq0nVsB9iRxCD3Vu"
st.write("We use the dataset [Migration Pattern of Young Adults](%s) to explore migration patterns of young people such as inbound rate and outbound rates for different states, average migration rate, popular migration routs and etc. "%uu)

st.write("We also use another three datasets to explore factors that we thought might affect migration rates including household income, education resources and job market.")


st.header("⬅️ Explore the data on each page in the sidebar!")
