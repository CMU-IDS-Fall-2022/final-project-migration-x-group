from logzero import logger

import pandas as pd
import streamlit as st

import data_munging
import plot_migration

from data_munging import ALL_STATES_TITLE

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
st.subheader('Average miles of migration')

st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

##VIZ 2
st.header("Top 10 Popular Destinations")
st.write(
    """
    [VIZ TO BE INSERTED]
    """
)

##VIZ 3
st.header("Migration rate by state")
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

#NAVIGATION SIDEBAR
with st.sidebar:
    st.markdown('# Navigation')
    st.markdown('## Overview')
    st.markdown('## Average miles of migration')
    st.markdown('## Most/least popular destinations')
    st.markdown('## Migration rate by sate')
    st.markdown("## Factors influencing migration rate")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Parental Income")
    st.markdown("### &nbsp;&nbsp;&nbsp;&nbsp; Economy")
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
