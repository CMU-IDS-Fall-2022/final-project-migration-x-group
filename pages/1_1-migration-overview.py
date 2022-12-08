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
    st.markdown('## 1. Overview of Young Adult Migration')
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [1-1 Inbound vs Outbound Rates](#1-1-inbound-vs-outbound-rates)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [1-2 Migration by State](#1-2-migration-by-state)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [1-3 Popular Migration Routes](#1-3-popular-migration-routes)")

st.markdown("## 1. Overview of Young Adult Migration")
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