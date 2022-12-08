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


st.write(
    """ 
    Young adults entering the workforce are important to economic development, but some states in the U.S. see more migration of young adults than others, leading to inequities in workforce development. \
    Therefore, we propose an interactive data science application that allows stakeholders in economic development to interpret migration patterns of young adults from their state.
    """
)

st.write(" Do you ever wonder how far people migrate between childhood and young adulthood? Where do they go? How much does one's location during childhood determine the labor markets that \
one is exposed to in young adulthood?We want to explore these questions using publicly available statistics on the migration patterns of young adults in the United States. \
Use this resource to discover where people in your hometown moved as young adults. What are the reasons behind young adult migration? Is it related to parental income, \
schooling or job market?")

st.markdown(" We conduct a state-level analysis of [The Migration Pattern of Young Adults dataset](https://www.census.gov/newsroom/press-kits/2022/young-adult-migration.html) from the Census Bureau.")
if st.checkbox("See Pivot Table of Migration Pattern of Young Adults Dataset"):
    main_dataset = load_data('data/state_level_migration.csv')
    st.write(main_dataset)

st.header("⬅️ Explore the data on each page in the sidebar!")
