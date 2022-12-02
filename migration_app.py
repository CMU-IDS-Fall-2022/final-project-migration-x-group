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
with st.expander('\U0001F609 Insights'):
    st.subheader("Race Black has the highest average migration rate across U.S.")

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

## outbound migration
state_out_migr_rate_sorted = state_lvl_migr_rate.sort_values(by=['outbound_rate'],ascending = False)
st.subheader("Top 5 states per Outbound Migration Rate:")
st.write(state_out_migr_rate_sorted.head(5)) 
    

st.text("Top 1 state with highest outbound migration rate is New Hampshire")

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
st.write('Massachussetts, Maine and New York are the top 3 destination states for young adult of New Hampshire migrated to.')

## Inbound Migration
st.subheader("Top 5 states with highest inbound migration rate :")
state_in_migr_rate_sorted = state_lvl_migr_rate.sort_values(by=['inbound_rate'],ascending = False)
st.write(state_in_migr_rate_sorted.head(5))
d_state = state_migration_pivot[['o_state_name','Colorado', 'Nevada']]
st.write(d_state)

d_state_filter1 = d_state.query("(o_state_name != 'Colorado')")
bar_inbound1 = alt.Chart(d_state_filter1).mark_bar(size=10).encode(
    x= alt.X('o_state_name:N', sort = '-y', axis = alt.Axis(title = 'original state') ),
    y= alt.Y('Colorado:Q')
).configure_mark(
    opacity = 0.8,
    color = 'brown'
)
st.write(bar_inbound1)

d_state_filter2 = d_state.query("(o_state_name != 'Nevada')")
bar_inbound2 = alt.Chart(d_state_filter2).mark_bar(size=10).encode(
    x= alt.X('o_state_name:N', sort = '-y', axis = alt.Axis(title = 'original state') ),
    y= alt.Y('Nevada:Q')
).configure_mark(
    opacity = 0.8,
    color = 'pink'
)
st.write(bar_inbound2)

st.markdown(':smile:')
if st.button('Click me to see Insights'):
    st.write("Colorado and Nevada are the top 2 popular states for young adults migrated to. And most of the young adults are from California.\
             By viewing the two charts above, we can see that Nevada's young adult migration pattern is very skewed, 43 percent from California. ")



st.subheader("Top 5 states with highest within_state migration rate are:")
state_lvl_migr_rate.sort_values(['within_state_rate'],ascending = False, inplace = True)
st.write(state_lvl_migr_rate.head(5))
st.markdown("Young adults from California tend to stay at their home state compared to young adults from other states")

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
st.subheader("How does employment rate of each CZ affect migration?")
st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

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



