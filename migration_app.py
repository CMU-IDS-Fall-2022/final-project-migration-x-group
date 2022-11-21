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
from matplotlib import pyplot as plt
import seaborn as sns



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
st.title("Reasons for Young Adult Migration")

st.header("Overview")


##VIZ 1
st.subheader('Overview of Young Adult Migration')

st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

##VIZ 2
st.subheader("Average Migration Rate By State and Race")
'''
# 1. loading dataset

od_race = load_data('od_race.csv')
st.text("Let's look at the dataset - count and fractions of people who move between each origin and destination commuting zone pair separately by race")

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
st.subheader("Race Black has the highest average migration rate across U.S.")

##VIZ 3
st.subheader("Migration Rate by State")
st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

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
st.subheader("How does median household income of each CZ affect correlate with migration rate?")
st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

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
'''
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
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; [Economy](#economy)")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Education")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Job Market")

###############################
## TEMPLATE EXAMPLE ##
TABLE_PAGE_LEN = 10

state_coordinates = data_munging.get_coordinates()
state_migration = pd.read_csv("data/state_migration.csv")
state_summary = pd.read_csv("data/state_migration_summary.csv")

st.title("State Movement")
state_choices = list(state_coordinates["name"])
state_choices.insert(0, ALL_STATES_TITLE)


with st.sidebar.form(key="my_form"):
    selectbox_state = st.selectbox("Choose a state", state_choices)
    selectbox_direction = st.selectbox("Choose a direction", ["Incoming", "Outgoing"])
    numberinput_threshold = st.number_input(
        """Set top N Migration per state""",
        value=3,
        min_value=1,
        max_value=25,
        step=1,
        format="%i",
    )

    st.markdown(
        '<p class="small-font">Results Limited to top 5 per State in overall US</p>',
        unsafe_allow_html=True,
    )
    pressed = st.form_submit_button("Build Migration Map")

expander = st.sidebar.expander("What is this?")
expander.write(
    """
This app allows users to view migration between states from 2018-2019.
Overall US plots all states with substantial migration-based relationships with other states.
Any other option plots only migration from or to a given state. This map will be updated
to show migration between 2019 and 2020 once new census data comes out.

Incoming: Shows for a given state, the percent of their **total inbound migration from** another state.

Outgoing: Shows for a given state, the percent of their **total outbound migration to** another state.
"""
)

# mig1 = plot_migration.build_migration_chart(G)
# mig_plot = st.plotly_chart(mig1)

network_place, _, descriptor = st.columns([6, 1, 3])

network_loc = network_place.empty()


# Create starting graph

descriptor.subheader(data_munging.display_state(selectbox_state))
descriptor.write(data_munging.display_state_summary(selectbox_state, state_summary))


edges = data_munging.compute_edges(
    state_migration,
    threshold=numberinput_threshold,
    state=ALL_STATES_TITLE,
    direction=selectbox_direction,
)


nodes = data_munging.compute_nodes(
    state_coordinates, edges, direction=selectbox_direction
)
G = data_munging.build_network(nodes, edges)
logger.info("Graph Created, doing app stuff")

migration_plot = plot_migration.build_migration_chart(G, selectbox_direction)
network_loc.plotly_chart(migration_plot)

st.write(
    """
    Hope you like the map!
    """
)

st.header("Migration Table")
table_loc = st.empty()
clean_edges = data_munging.table_edges(edges, selectbox_direction)
table_loc.table(clean_edges.head(20))

if pressed:
    edges = data_munging.compute_edges(
        state_migration,
        threshold=numberinput_threshold,
        state=selectbox_state,
        direction=selectbox_direction,
    )

    nodes = data_munging.compute_nodes(
        state_coordinates, edges, direction=selectbox_direction
    )
    # st.table(nodes[["name", "latitude", "Migration"]].head(10))
    G = data_munging.build_network(nodes, edges)
    # st.table(G.edges)
    migration_plot = plot_migration.build_migration_chart(G, selectbox_direction)
    network_loc.plotly_chart(migration_plot)

    clean_edges = data_munging.table_edges(edges, selectbox_direction)
    table_loc.table(clean_edges.head(20))



## Economy
st.header("Economy")
st.subheader("How do median household incomes of each state affect migration?")


df_income = median_income_process.get_income_df()
scatter_income = alt.Chart(df_income).mark_circle(size=50).encode(
    x='mean',
    y='outbound_migration',
    tooltip=['state_name','mean','outbound_migration']
).interactive()

scatter_income.title = 'Outbound Migration Number and Average Median Household Income by State'
st.write(scatter_income)

st.write("Correlation Analysis")
st.write("[some table / text describing the correlation]")