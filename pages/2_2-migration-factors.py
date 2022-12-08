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

#NAVIGATION SIDEBAR
with st.sidebar:
    st.markdown("## 2. Factors influencing migration rate")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [2-1 Household Income](#2-1-household-income)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [2-2 Education](#2-2-education)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [2-3 Job Market](#2-3-job-market)")

##VIZ 4
st.header("2. Factors influencing migration rate")

##VIZ 4-1
## Economy
st.header("2-1 Household Income")
st.subheader("How do median household incomes affect each state's inbound migration rate?")
st.write("The economic level of an area has a great influence on people's motivation to migrate in. Therefore, we choose the household income as a major aconomic metrics and expore its relationship with the inbound migration rate.")
url = "https://www.census.gov/data/datasets/2010/demo/saipe/2010-state-and-county.html"

st.write("The household income data comes from the [SAIPE ‘State and County Estimates’ Datasets](%s) on the United States Census Bureau website."%url)
st.markdown(
        """
        We calculate the Average Household Income as follows:
        -  `Avergae Household Income = Average(household income median from 2010 to 2018)`
        """
    )

df_income = load_data("data/state_income_for_viz.csv")
df_income =df_income.rename(columns={"average_from_2010": "Average Household Income"})
df_income =df_income.rename(columns={"state_name": "State"})
df_income =df_income.rename(columns={"inbound_migration_rate": "Inbound Migration Rate"})
df_income_backup = df_income
income_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')
migration_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')

choropleth = folium.Choropleth(
    geo_data='us-state-boundaries.geojson',
    data=df_income,
    columns=('State', 'Average Household Income'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True,
)

choropleth1 = folium.Choropleth(
    geo_data='us-state-boundaries.geojson',
    data=df_income,
    columns=('State', 'Inbound Migration Rate'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True,
)
choropleth.geojson.add_to(income_map)
choropleth1.geojson.add_to(migration_map)

df_income = df_income.set_index('State')
for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['income'] = 'household income: ' + str(df_income.loc[state_name, 'Average Household Income'] 
                                                                    if state_name in list(df_income.index) else 'N/A')
      
for feature in choropleth1.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['migration'] = 'inbound rate: ' + str(df_income.loc[state_name, 'Inbound Migration Rate'] 
                                                                    if state_name in list(df_income.index) else 'N/A')

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','income'], labels=False)
)

choropleth1.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','migration'], labels=False)
)

cols = st.columns(2)
with cols[0]:
    st.write("#### Average Household Income for all States in the United States")
    left = st_folium(income_map, width=420, height=300)
with cols[1]:
    st.write("#### Inbound Migration Rates for all States in the United States")
    right = st_folium(migration_map, width=420, height=300)

df_income = load_data("data/state_income_for_viz.csv")

scatter_income = alt.Chart(df_income_backup).mark_circle(size=50).encode(
    x='Average Household Income:Q',
    y='Inbound Migration Rate:Q',
    tooltip=['State','Average Household Income','Inbound Migration Rate']
).properties(
    height = 400,
    width = 600,
).interactive()

scatter_income.title = 'Inbound Migration Rate and Average Median Household Income Median by State'
st.write(scatter_income)

st.write("#### Correlation Analysis")
correlation = median_income_process.calculateCorrelation(df_income_backup)
st.write("Pearson correlation coefficient")
st.write(correlation)
st.write("Therefore there is no visible correlation between each state's inbound migration rate and average household income median.")

##VIZ 4-2
## Education
st.header("2-2 Education")
st.subheader("Explore the Correlation Between Inbound Migration Rate with Educational Ratio in All States in the United States")

st.write("Young people have a strong motivation to move from one area to another if the education is of high quality. \
          We will investigate the correlation between educational attainment and the rate of immigration into all US states in this section. \
          To examine the correlation, we will first plot the educational ratio and the inbound migration rate for each state side by side.")

url = "https://data.census.gov/table?q=education+by+county&tid=ACSDT1Y2021.B14001&moe=false&tp=false"

st.write("The educational data comes from the [SCHOOL ENROLLMENT BY LEVEL OF SCHOOL FOR THE POPULATION 3 YEARS AND OVER](%s) on the United States Census Bureau website."%url)
st.markdown(
        """
        We calculate the Educational Ratio as follows:
        -  `Educational Ratio = Average(educational ratio from 2013 to 2018)`
        """
    )

df_education = load_data("data/Educational_Migration.csv")
df_migration = load_data("data/state_migration_summary.csv")

education_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')
migration_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')

choropleth = folium.Choropleth(
    geo_data='data/us-state-boundaries.geojson',
    data=df_education,
    columns=('state', 'average'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    fill_color='YlGnBu',
    highlight=True,
)

choropleth1 = folium.Choropleth(
    geo_data='data/us-state-boundaries.geojson',
    data=df_migration,
    columns=('state', 'inbound_migration_rate'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    fill_color='YlOrRd',
    highlight=True,
)
choropleth.geojson.add_to(education_map)
choropleth1.geojson.add_to(migration_map)

df_education=df_education.set_index('state')
df_migration=df_migration.set_index('state')

for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['education'] = 'educational ratio: ' + str(df_education.loc[state_name, 'average'] 
                                                                    if state_name in list(df_education.index) else 'N/A')
      
for feature in choropleth1.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['migration'] = 'inbound migration rate: ' + str(df_migration.loc[state_name, 'inbound_migration_rate'] 
                                                                    if state_name in list(df_migration.index) else 'N/A')

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','education'], labels=False)
)

choropleth1.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','migration'], labels=False)
)

cols = st.columns(2)
with cols[0]:
    st.write("#### Average Educational Ratio from 2013-2018 for all States in the United States")
    left = st_folium(education_map, width=420, height=300)
with cols[1]:
    st.write("#### Average Inbound Migration Rates from 2010-2021 for all States in the United States")
    right = st_folium(migration_map, width=420, height=300)


st.subheader("How does the educational ratio of each state affect young people's choice of migration destination?")
#fig = px.scatter(
    #data_frame=df_education, x="average", y="inbound_migration_rate", title="Correlation Between Educational Ratio and Inbound Migration Rate in All States",
#)
#st.plotly_chart(fig)
df_education = df_education.reset_index()
df_education.rename(columns={'average':'educational_ratio'}, inplace=True)
scatter_education = alt.Chart(df_education).mark_circle(size=50).encode(
    x='educational_ratio:Q',
    y='inbound_migration_rate:Q',
    tooltip=['state','educational_ratio','inbound_migration_rate']
).properties(
    height = 400,
    width = 600,
).interactive()

scatter_education.title = 'Correlation Between Educational Ratio and Inbound Migration Rate in All States'
st.write(scatter_education)

st.write("#### Correlation Analysis")
correlation = df_education['inbound_migration_rate'].corr(df_education['educational_ratio'])
c = str(round(correlation, 2))
st.write("Pearson correlation coefficient bewteen educational ratio and inbound migration rate is:")
st.write(c)
st.write("Therefore, there is no visible correlation between each state's inbound migration rate and the educational ratio.")




##VIZ 4-3
################################################### Job Market and Migration Rate ###########################################
st.header("2-3 Job Market")
st.subheader("Explore the Correlation Between Migration Rate with Employment Rate in All States in the United States")
st.write("As we all know, good job market is a great incentive for people to migrate from one place to another. \
          In this section, we intend to explore the correlation between the employment rate and migrate in rates in all US states. \
          We will first try to map employment rate and migrate in rate in the granularity of states side by side to explore this correlation.")

urlll = "https://data.census.gov/table?q=job+opening+by+county&tid=ACSDP1Y2021.DP03"

st.write("The employment data comes from the [ACS 5-Year Estimates Equal Employment Opportunity](%s) on the United States Census Bureau website."%urlll)
st.markdown(
        """
        We calculate the Educational Ratio as follows:
        -  `Employment Ratio = Average(employment ratio from 2010 to 2021)`
        """
    )
# df = pd.read_csv('data/employment_migration_vis.csv')
df = load_data('data/employment_migration_vis.csv')
if st.checkbox("Show Employment and Migration Data"):
    st.write(df)
# st.write(df)
df.rename(columns={df.columns[0]:'index'}, inplace=True)
df.rename(columns={df.columns[4]:'inbound_rate'}, inplace=True)
df = df.round({'employment_rate': 2})
df['employment_rate'] = df['employment_rate'].div(100).round(2)
df = df.round({'inbound_rate': 2})
dropp = df[df.state == 'Puerto Rico'].index
df = df.drop(dropp)
df1 = df
# st.write(df1)
# if st.checkbox("Show Employment and Migration Data"):
#     st.write(df)


employment_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')
migration_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')

choropleth = folium.Choropleth(
    geo_data='us-state-boundaries.geojson',
    data=df,
    columns=('state', 'employment_rate'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True,
)

choropleth1 = folium.Choropleth(
    geo_data='us-state-boundaries.geojson',
    data=df,
    columns=('state', 'inbound_rate'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True,
)
choropleth.geojson.add_to(employment_map)
choropleth1.geojson.add_to(migration_map)

df = df.set_index('state')
for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['employment'] = 'employment rate: ' + str(df.loc[state_name, 'employment_rate'] 
                                                                    if state_name in list(df.index) else 'N/A')
      
for feature in choropleth1.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['migration'] = 'inbound rate: ' + str(df.loc[state_name, 'inbound_rate'] 
                                                                    if state_name in list(df.index) else 'N/A')

choropleth.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','employment'], labels=False)
)

choropleth1.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','migration'], labels=False)
)

cols = st.columns(2)
with cols[0]:
    st.write("#### Average Employment Rates from 2010-2021 for all States in the United States")
    left = st_folium(employment_map, width=420, height=300)
with cols[1]:
    st.write("#### Average Inbound Rates from 2010-2021 for all States in the United States")
    right = st_folium(migration_map, width=420, height=300)

st.write("From the two maps shown above, we can see that there are some correlation between employment rate and migrate in rate. In the central north areas,\
           high employment rate coexists with high migration in rate, especially in states of Wyoming, North Dakota and Corolado. The same correlation also \
           shows up in Northeast and Southeast coast of US. To further explore the correlation, we try to plot 52 states' employment rate and migration in rate in the same chart. \
           We also drop two outliers of Delaware and Puerto Rico to increase the accuracy of the correlation coeffient.")

#Drop outliner of Delaware and Puerto Rico
drop2 = df1[df1.state == 'Puerto Rico'].index
df1 = df1.drop(drop2)

bar_chart =  alt.Chart(df1).mark_point().encode(
                                x = "employment_rate",
                                y = "inbound_rate",
                                tooltip=['state', 'employment_rate', 'inbound_rate']
                                ).properties(
                                    width=860, height=400,
                                )

st.subheader("Correlation Between Employment Rate and Inbound Rate in All States")
st.write(bar_chart)
st.write("#### Correlation Analysis")
correlation = df1['employment_rate'].corr(df1['inbound_rate'])
c = str(round(correlation, 2))
st.write("Pearson correlation coefficient bewteen employment rate and inbound rate is:")
st.write(c)
st.write("From the plot chart above, we can see the correlation coefficient is 0.1, so there is a very week positive correlation between inbound rate and the Employment rate. From this week correlation, we can extrapolate that there might be other factors influence people's decision to migrate one state to another. That is to say employement rate is not the only and determing factor.")


