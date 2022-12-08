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


## NEW PROJECT START ##
st.title("U.S. Young Adult Migration Analysis")

#NAVIGATION SIDEBAR
with st.sidebar:
    st.markdown('## 1. Overview of Young Adult Migration')
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [1-1 Inbound vs Outbound Rates](#1-1-inbound-vs-outbound-rates)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [1-2 Migration by State](#1-2-migration-by-state)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [1-3 Popular Migration Routes](#1-3-popular-migration-routes)")
    st.markdown("## 2. Factors influencing migration rate")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [2-1 Household Income](#2-1-household-income)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [2-2 Education](#2-2-education)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [2-3 Job Market](#2-3-job-market)")


# Main
## Viz 1-1

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

# st.write(" The dataset we are using for doing the analysis is the The Migration Pattern of Young Adults.")
# if st.checkbox("The Migration Pattern of Young Adults Dataset"):
#     main_dataset = load_data('data/state_level_migration.csv')
#     st.write(main_dataset)

## Viz 1-1
st.markdown("### 1-1 Inbound vs Outbound Rates")
overview.show_inbound_vs_outbound_maps()
## Viz 1-2
st.markdown("### 1-2 Migration by State")
overview.show_state_by_state_migration()

##VIZ 2
st.subheader("1-2-1 Average Migration Rate By State and Race")

# 1. loading dataset
# the original od_race file size is too big (>100MB), so divide the big file into several files(<25MB) then load and combine individual dataframe
od_race1 = load_data('data/od_race_1.csv')
od_race2 = load_data('data/od_race_2.csv')
od_race3 = load_data('data/od_race_3.csv')
od_race4 = load_data('data/od_race_4.csv')
od_race5 = load_data('data/od_race_5.csv')
od_race6 = load_data('data/od_race_6.csv')
od_race7 = load_data('data/od_race_7.csv')
od_race8 = load_data('data/od_race_8.csv')
od_race9 = load_data('data/od_race_9.csv')
od_race10 = load_data('data/od_race_10.csv')
od_race11 = load_data('data/od_race_11.csv')
od_race12 = load_data('data/od_race_12.csv')
od_race13 = load_data('data/od_race_13.csv')
od_race14 = load_data('data/od_race_14.csv')
od_race15 = load_data('data/od_race_15.csv')
od_race16 = load_data('data/od_race_16.csv')
od_race17 = load_data('data/od_race_17.csv')

od_race = pd.concat([od_race1,od_race2,od_race3,od_race4,od_race5,od_race6,od_race7,od_race8,od_race9,od_race10,od_race10,od_race12,od_race13,od_race14,od_race15,od_race16,od_race17 ],
ignore_index = True, sort = False)

# 2. show dataframe or not
if st.checkbox("Show Raw Data"):
    st.write(od_race.head(5))

# 3. Insights from Data
od_race['condition'] = np.where((od_race['o_cz'] == od_race['d_cz']), 'remove', 'keep')
sorted = od_race.sort_values(by = ['condition'], ascending = False)
df1 = od_race.groupby(['o_state_name','pool','condition']).agg({'n':['mean', 'sum']})
df1.columns = ['n_mean', 'n_sum']
df1 = df1.reset_index()

df_group = od_race.groupby(['o_state_name','pool']).agg({'n':['sum']})
df_group = df_group.reset_index()
df_group_con = pd.concat([df_group]*2, ignore_index=True) # to have same # of records as df1

df_group_con.columns = df_group_con.columns.get_level_values(0)  # to solve nested index
df_group_sorted = df_group_con.sort_values(['o_state_name', 'pool'])
df_group_sorted = df_group_sorted.reset_index()

df1_sorted = df1.sort_values(['o_state_name', 'pool'])
df1_sorted['rate'] =  df1_sorted['n_sum'] / df_group_sorted['n']
df1_cz_rate = df1_sorted \
                   .query("(condition == 'keep')") \
                   .groupby(['o_state_name', 'pool'], as_index = False) \
                   .agg(average_rate = ("rate" , 'mean')) 


# The below code is adapted from https://altair-viz.github.io/gallery/multiline_highlight.html
highlight = alt.selection(type='single', on='mouseover',
                          fields=['pool'], nearest=True)
rate_by_state_race = alt.Chart(df1_cz_rate).encode(
                                              x='o_state_name:N',
                                              y='average_rate:Q',
                                              color='pool:N'
                    )
points = rate_by_state_race.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
).properties(
    width=1200
)
lines = rate_by_state_race.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)
st.write(points + lines)
st.markdown("##### \U0001F348 Race Black reached its peak in Hawaii; race Asian reached its peak in Kansas and race Hispanic reached its peak in Vermont.From website https://files.hawaii.gov/dbedt/census/Census_2010/SF1/Hawaii_Population_Facts_6-2011.pdf, it also shows that from 2000 to 2010, Black or African American population dropped 2.6%.")
st.markdown ("##### On the other side, race Black's lowest point is in Maryland; race Hispanic's lowest point is in Illinois; race Asian's lowest point is in New York.")
st.text("The sample includes all children who are born in the U.S. between 1984-92, and tracked individual's migration activity from age 16 to age 26. \n" 
        "For these participants, age 16 corresponds to the year from 2000 to 2008.")
##VIZ 3 
st.markdown("### 1-3 Popular Migration Routes")
state_lvl_migr = load_data("data/state_migration_summary.csv")
state_lvl_migr_rate = state_lvl_migr.copy()
state_lvl_migr_rate['total'] = state_lvl_migr_rate['inbound_migration'] + state_lvl_migr_rate['outbound_migration'] + state_lvl_migr_rate['within_state_migration']
state_lvl_migr_rate['inbound_rate'] = state_lvl_migr_rate['inbound_migration'] / state_lvl_migr_rate['total']
state_lvl_migr_rate['outbound_rate'] = state_lvl_migr_rate['outbound_migration'] / state_lvl_migr_rate['total']
state_lvl_migr_rate['within_state_rate'] = state_lvl_migr_rate['within_state_migration'] / state_lvl_migr_rate['total']
# convert data type from object to int 
state_lvl_migr_rate['inbound_rate'].astype(str).astype(float)
state_lvl_migr_rate['outbound_rate'].astype(str).astype(float)
state_lvl_migr_rate['within_state_rate'].astype(str).astype(float)

################################################ Outbound Migration ###################################################
st.markdown("#### 1-3-1 Outbound Migration Pattern Analysis")
state_out_migr_rate_sorted = state_lvl_migr_rate.sort_values(by=['outbound_rate'],ascending = False)
state_out_migr_rate_sorted = state_out_migr_rate_sorted[['state', 'outbound_migration', 'outbound_rate']]
most = state_out_migr_rate_sorted.head(5)

state_out_migr_rate_least = state_lvl_migr_rate.sort_values(by=['outbound_rate'],ascending = True)
state_out_migr_rate_least = state_out_migr_rate_least[['state', 'outbound_migration', 'outbound_rate']]
least = state_out_migr_rate_least.head(5)
# Go horizontal with columns: referenced from https://blog.streamlit.io/introducing-new-layout-options-for-streamlit/
cols = st.columns(2)
with cols[0]:
    st.write(most, use_column_width=True)
    st.text("Top 5 most popular states per Outbound Migration Rate")
with cols[1]:
    st.write(least,use_column_width=True)
    st.text("Top 5 least popular states per Outbound Migration Rate")

st.markdown("##### Top 1 state with highest outbound migration rate is New Hampshire")
st.markdown('##### Let Us Discover Popular Routes for New Hampshire')
state_migration_pivot = load_data("data/state_migration_pivot.csv")
nh = state_migration_pivot\
             .query("(o_state_name  == 'New Hampshire')")

nh_transposed = nh.T
nh_transposed = nh_transposed.reset_index()
new_header1 = nh_transposed.iloc[0] #grab the first row for the header
nh_transposed = nh_transposed[1:] #take the data less the header row
nh_transposed.columns = new_header1 #set the header row as the df header
nh_transposed_filter = nh_transposed.query("(o_state_name  != 'New Hampshire')")

bar_outbound = alt.Chart(nh_transposed_filter).mark_bar(size=10).encode(
    x= alt.X('o_state_name:N', sort = '-y', axis = alt.Axis(title = 'destination state') ),
    y= alt.Y('New Hampshire:Q')
)
text = bar_outbound.mark_text(
    align='left',
    baseline='middle',
    dx=3  # Nudges text to right so it doesn't appear on top of the bar
).encode(
    text='New Hampshire:Q')

st.write(
    bar_outbound
)
st.markdown('##### \U0001F348 Massachussetts, Maine and New York are the top 3 destination states for young adult of New Hampshire migrated to.')
df_education_2008 = load_data("data/2008 Grading Summary.csv")
df_migration = load_data("data/state_migration_summary.csv")

education_map = folium.Map(location=[38, -96.5], zoom_start=3.4, scrollWheelZoom=False, tiles='CartoDB positron')
choropleth_grade = folium.Choropleth(
    geo_data='data/us-state-boundaries.geojson',
    data=df_education_2008,
    columns=('state', 'score'),
    key_on='feature.properties.name',
    line_opacity=0.8,
    fill_color='YlGnBu',
    highlight=True,
)
choropleth_grade.geojson.add_to(education_map)

df_education=df_education_2008.set_index('state')

for feature in choropleth_grade.geojson.data['features']:
    state_name = feature['properties']['name']
    feature['properties']['education'] = 'education score: ' + str(df_education.loc[state_name, 'score'] 
                                                                    if state_name in list(df_education.index) else 'N/A')
choropleth_grade.geojson.add_child(
    folium.features.GeoJsonTooltip(['name','education'], labels=False)
)

st.write("##### Educational Score in 2018 for all States in the United States")
left = st_folium(education_map, width=600, height=400)
right = st.write('Massachussetts and New York have the highest gradings in 2008') 
st.write("data source: https://www.edweek.org/policy-politics/grading-the-states/2008/01")

# Correlation 
df_migration = load_data("data/state_migration_summary.csv")
df_higher_education = load_data("data/Higher_Edu_RatioByState.csv")

correlation = df_migration['inbound_migration_rate'].corr(df_higher_education['higher_edu_ratio'])
c1 = str(round(correlation,3))
st.markdown('##### corrleation score:' + c1)
st.markdown("##### \U0001F348 There is a positive relationship between higher education ratio and inbound migration rate.") 


################################################ Inbound Migration ###################################################
st.markdown("#### 1-3-2 Inbound Migration Pattern Analysis")
state_in_migr_rate_sorted = state_lvl_migr_rate.sort_values(by=['inbound_rate'],ascending = False)
state_in_migr_rate_sorted = state_in_migr_rate_sorted[['state', 'inbound_migration', 'inbound_rate']]
most = state_in_migr_rate_sorted.head(5)

state_in_migr_rate_least = state_lvl_migr_rate.sort_values(by=['inbound_rate'],ascending = True)
state_in_migr_rate_least = state_in_migr_rate_least[['state', 'inbound_migration', 'inbound_rate']]
least = state_in_migr_rate_least.head(5)

cols = st.columns(2)
with cols[0]:
    st.write(most, use_column_width=True)
    st.text("Top 5 most popular states per Inbound Migration rate")
with cols[1]:
    st.write(least,use_column_width=True)
    st.text('Top 5 least popular states per Inbound Migration Rate')

st.markdown('##### Discover the migration routes for the top 2 popular states')
d_state = state_migration_pivot[['o_state_name','Colorado', 'Nevada']]
st.write(d_state)
d_state_filter1 = d_state.query("(o_state_name != 'Colorado')")
bar_inbound1 = alt.Chart(d_state_filter1).mark_bar(size=10).encode(
    x= alt.X('o_state_name:N', sort = '-y', axis = alt.Axis(title = 'original state') ),
    y= alt.Y('Colorado:Q')
).configure_mark(
    opacity = 1,
    color = 'purple'
)
st.write(bar_inbound1)

d_state_filter2 = d_state.query("(o_state_name != 'Nevada')")
bar_inbound2 = alt.Chart(d_state_filter2).mark_bar(size=10).encode(
    x= alt.X('o_state_name:N', sort = '-y', axis = alt.Axis(title = 'original state') ),
    y= alt.Y('Nevada:Q')
).configure_mark(
    opacity = 1,
    color = 'pink'
)
st.write(bar_inbound2)

#with st.expander('\U0001F348 Click Me for Insights'):
st.markdown("##### \U0001F348 Colorado and Nevada are the top 2 popular states for young adults migrated to. And most of them are from California.\
             By viewing the two charts above, we can see that Nevada's young adults migration pattern is very skewed, 43 percent coming from California. \
             In addition, Texas ranks #2 for both Colorado and Nevada but more young adults from Texas migrated to Colorado than Nevada.")

################################################ within state rate ###################################################
st.markdown("#### 1-3-3 Within State Migration Pattern Analysis")
state_lvl_migr_rate.sort_values(['within_state_rate'],ascending = False, inplace = True)
state_with_migr_rate_sorted = state_lvl_migr_rate[['state', 'within_state_migration', 'within_state_rate']]
most = state_with_migr_rate_sorted.head(5)

state_lvl_migr_rate.sort_values(['within_state_rate'],ascending = True, inplace = True)
state_with_migr_rate_least = state_lvl_migr_rate[['state', 'within_state_migration', 'within_state_rate']]
least = state_with_migr_rate_least.head(5)
cols = st.columns(2)
with cols[0]:
    st.write(most, use_column_width=True)
    st.text("Top 5 most popular states per within_state migration rate are:")
with cols[1]:
    st.write(least,use_column_width=True)
    st.text("Top 5 least popular states per within_state migration rate are")

st.markdown("##### \U0001F348 Young adults from California tend to stay at their home state compared to young adults from other states; \
              whereas young adults from Wyoming tend to move out.")


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
df = pd.read_csv('data/employment_migration_vis.csv')
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


