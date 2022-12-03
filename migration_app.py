import data_munging
import median_income_process
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

# Main
st.title("Reasons for Young Adult Migration")

st.header("Overview")


##VIZ 1 - OVERVIEW MAP
st.subheader('Overview of Young Adult Migration')

#Display overview state migration map
#library quickstart https://python-visualization.github.io/folium/quickstart.html#Choropleth-maps
state_lvl_migr = pd.read_csv("data/state_level_migration.csv")
map = folium.Map(location=[38, -96.5], zoom_start=4, scrollWheelZoom=False, tiles='CartoDB positron') #Creating Folium MNap

choropleth = folium.Choropleth(
    geo_data='data/us-state-boundaries.geojson',
    data=state_lvl_migr,
    columns=(list(state_lvl_migr.columns)),
    key_on='feature.properties.name',
    line_opacity=0.8,
    highlight=True
)

for feature in choropleth.geojson.data['features']:
    state_name = feature['properties']['name']
    #TODO: Add features from the dataframe to geojson file
    #feature['properties']['population'] = 'Population: ' + '{:,}'.format(df_indexed.loc[state_name, 'State Pop'][0]) if state_name in list(df_indexed.index) else ''
    #feature['properties']['per_100k'] = 'Reports/100K Population: ' + str(round(df_indexed.loc[state_name, 'Reports per 100K-F&O together'][0])) if state_name in list(df_indexed.index) else ''

choropleth.geojson.add_child(
         folium.features.GeoJsonTooltip(['name'], labels=False)
     )

choropleth.geojson.add_to(map)

st_map = st_folium(map, width=700, height=450) 

state_name = ''
if st_map['last_active_drawing']:
    state_name = st_map['last_active_drawing']['properties']['name']

if st.checkbox("Show pivot table"):
    st.write(state_lvl_migr)

#TODO: Insert Bar Chart of Destinations from selected State
#st.bar_chart(state_lvl_migr)

st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

##VIZ 2
st.subheader("Average Migration Rate By State and Race")

# 1. loading dataset
# the original od_race file size is too big (>100MB), so divide the big file into several files(<25MB) then load and combine individual dataframe
od_race1 = pd.read_csv('data/od_race_1.csv')
od_race2 = pd.read_csv('data/od_race_2.csv')
od_race3 = pd.read_csv('data/od_race_3.csv')
od_race4 = pd.read_csv('data/od_race_4.csv')
od_race5 = pd.read_csv('data/od_race_5.csv')
od_race6 = pd.read_csv('data/od_race_6.csv')
od_race7 = pd.read_csv('data/od_race_7.csv')
od_race8 = pd.read_csv('data/od_race_8.csv')
od_race9 = pd.read_csv('data/od_race_9.csv')
od_race10 = pd.read_csv('data/od_race_10.csv')
od_race11 = pd.read_csv('data/od_race_11.csv')
od_race12 = pd.read_csv('data/od_race_12.csv')
od_race13 = pd.read_csv('data/od_race_13.csv')
od_race14 = pd.read_csv('data/od_race_14.csv')
od_race15 = pd.read_csv('data/od_race_15.csv')
od_race16 = pd.read_csv('data/od_race_16.csv')
od_race17 = pd.read_csv('data/od_race_17.csv')

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
with st.expander('\U0001F348 Insights'):
    st.subheader("Race Black reached its peak in Hawaii; Asian reached its peak in Kansas and Hispanic reached its peak in Vermont. ")

##VIZ 3
st.header("Popular Migration Routes")
state_lvl_migr = pd.read_csv("data/state_migration_summary.csv")
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

st.subheader("Top 1 state with highest outbound migration rate is New Hampshire")
st.subheader('Let Us Discover popular routes for New Hampshire')
state_migration_pivot = pd.read_csv("data/state_migration_pivot.csv")
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
st.subheader('Massachussetts, Maine and New York are the top 3 destination states for young adult of New Hampshire migrated to.')

################################################ Inbound Migration ###################################################

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

st.subheader('Discover the migration routes for the top 2 popular states')
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

with st.expander('\U0001F348 Click Me for Insights'):
    st.write("Colorado and Nevada are the top 2 popular states for young adults migrated to. And most of the young adults are from California.\
             By viewing the two charts above, we can see that Nevada's young adult migration pattern is very skewed, 43 percent from California; ")

################################################ within state rate ###################################################
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

st.subheader("Young adults from California tend to stay at their home state compared to young adults from other states")

##VIZ 4
st.header("Factors influencing migration rate")

##VIZ 4-1
st.subheader("How does parental income affect migration rate?")
st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

##VIZ 4-2
## Economy
st.header("Economy - Household Income")
st.subheader("How do median household incomes affect each state's migration?")

df_income = pd.read_csv("data/state_income_for_viz.csv")
scatter_income = alt.Chart(df_income).mark_circle(size=50).encode(
    x='average_household_income_median:Q',
    y='inbound_migration:Q',
    tooltip=['state_name','average_household_income_median','inbound_migration']
).properties(
    height = 400,
    width = 600,
).interactive()

scatter_income.title = 'Inbound Migration Number and Average Median Household Income Median by State'
st.write(scatter_income)

st.write("#### Correlation Analysis")
correlation = median_income_process.calculateCorrelation(df_income)
st.write("Pearson correlation coefficient")
st.write(correlation)
st.write("Therefore there is no visible correlation between each state's inbound migration and average household income median.")


##VIZ 4-3
st.subheader("How does education rate of each CZ affect young people choice of migration destination?")
st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

##VIZ 4-4
################################################### Job Market and Migration Rate ###########################################
st.header("Explore the Correlation Between Migration Rate with Employment Rate in All States in the United States")
st.write("As we all know, good job market is a great incentive for people to migrate from one place to another. \
          In this section, we intend to explore the correlation between the employment rate and migrate in rates in all US states. \
          We will first try to map employment rate and migrate in rate in the granularity of states side by side to explore this correlation.")

df = pd.read_csv('data/employment_migration.csv')
df.rename(columns={df.columns[0]:'index'}, inplace=True)
df.rename(columns={df.columns[4]:'inbound_rate'}, inplace=True)
df = df.round({'employment_rate': 2})
df = df.round({'inbound_rate': 2})
dropp = df[df.state == 'Puerto Rico'].index
df = df.drop(dropp)
df1 = df
if st.checkbox("Show Employment and Migration Data"):
    st.write(df)

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
           We also drop two outliers of Delaware and Puerto Rico to increase the accuracy of the correlation coeffient. ")

#Drop outliner of Delaware and Puerto Rico
drop1 = df1[df1.state == 'Delaware'].index
drop2 = df1[df1.state == 'Puerto Rico'].index
df1 = df1.drop(drop1)
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
st.write("From the plot chart above, we can see the correlation coefficient is 0.19, so there is a week positive correlation between migration in rate and the Employment rate. From this week correlation, \
         we can extrapolate that there might be other factors influence people's decision to migrate one state to another. That is to say employement rate is not the only and determing factor.")

#NAVIGATION SIDEBAR
with st.sidebar:
    st.markdown('# Navigation')
    st.markdown('## Overview')
    #st.markdown("[Overview](#overview)") #create an anchor link to the header overview
    st.markdown('## Average miles of migration')
    st.markdown('## Most/least popular destinations')
    st.markdown('## Migration rate by sate')
    st.markdown("## Factors influencing migration rate")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Parental Income")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [Economy - Household Income](#economy-household-income)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Education")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Job Market")

###############################
## TEMPLATE EXAMPLE ##
# TABLE_PAGE_LEN = 10

# state_coordinates = data_munging.get_coordinates()
# state_migration = pd.read_csv("data/state_migration.csv")
# state_summary = pd.read_csv("data/state_migration_summary.csv")

# st.title("State Movement")
# state_choices = list(state_coordinates["name"])
# state_choices.insert(0, ALL_STATES_TITLE)


# with st.sidebar.form(key="my_form"):
#     selectbox_state = st.selectbox("Choose a state", state_choices)
#     selectbox_direction = st.selectbox("Choose a direction", ["Incoming", "Outgoing"])
#     numberinput_threshold = st.number_input(
#         """Set top N Migration per state""",
#         value=3,
#         min_value=1,
#         max_value=25,
#         step=1,
#         format="%i",
#     )

#     st.markdown(
#         '<p class="small-font">Results Limited to top 5 per State in overall US</p>',
#         unsafe_allow_html=True,
#     )
#     pressed = st.form_submit_button("Build Migration Map")

# expander = st.sidebar.expander("What is this?")
# expander.write(
#     """
# This app allows users to view migration between states from 2018-2019.
# Overall US plots all states with substantial migration-based relationships with other states.
# Any other option plots only migration from or to a given state. This map will be updated
# to show migration between 2019 and 2020 once new census data comes out.

# Incoming: Shows for a given state, the percent of their **total inbound migration from** another state.

# Outgoing: Shows for a given state, the percent of their **total outbound migration to** another state.
# """
# )

# # mig1 = plot_migration.build_migration_chart(G)
# # mig_plot = st.plotly_chart(mig1)

# network_place, _, descriptor = st.columns([6, 1, 3])

# network_loc = network_place.empty()


# # Create starting graph

# descriptor.subheader(data_munging.display_state(selectbox_state))
# descriptor.write(data_munging.display_state_summary(selectbox_state, state_summary))


# edges = data_munging.compute_edges(
#     state_migration,
#     threshold=numberinput_threshold,
#     state=ALL_STATES_TITLE,
#     direction=selectbox_direction,
# )


# nodes = data_munging.compute_nodes(
#     state_coordinates, edges, direction=selectbox_direction
# )
# G = data_munging.build_network(nodes, edges)
# logger.info("Graph Created, doing app stuff")

# migration_plot = plot_migration.build_migration_chart(G, selectbox_direction)
# network_loc.plotly_chart(migration_plot)

# st.write(
#     """
#     Hope you like the map!
#     """
# )

# st.header("Migration Table")
# table_loc = st.empty()
# clean_edges = data_munging.table_edges(edges, selectbox_direction)
# table_loc.table(clean_edges.head(20))

# if pressed:
#     edges = data_munging.compute_edges(
#         state_migration,
#         threshold=numberinput_threshold,
#         state=selectbox_state,
#         direction=selectbox_direction,
#     )

#     nodes = data_munging.compute_nodes(
#         state_coordinates, edges, direction=selectbox_direction
#     )
#     # st.table(nodes[["name", "latitude", "Migration"]].head(10))
#     G = data_munging.build_network(nodes, edges)
#     # st.table(G.edges)
#     migration_plot = plot_migration.build_migration_chart(G, selectbox_direction)
#     network_loc.plotly_chart(migration_plot)

#     clean_edges = data_munging.table_edges(edges, selectbox_direction)
#     table_loc.table(clean_edges.head(20))
# ### END OF TEMPLATE



