import pandas as pd
import numpy as np
import streamlit as st
import altair as alt

@st.cache(allow_output_mutation=True)  # add caching so we load the data only once
def load_data(file_path):
    return pd.read_csv(file_path)

def get_income_df():
    df_sum = load_data("data/state_migration.csv")

    df_d = df_sum.groupby(['d_state_name']).agg({'n':'sum'})
    df_d = df_d.reset_index()
    df_income = load_data("data/state_household_income.csv")

    df_income = df_income.replace({'state_name': {'DC': 'District of Columbia'}})

    for i in range(len(df_income.index)):
        df_income.iloc[i,1] = df_income.iloc[i,1].upper()

    df_income = df_income.sort_values(by='state_name')
    df_income = df_income.reset_index(drop=True)
    df_sum = df_sum.sort_values(by='state')

    #print(df_sum['state'] == df_income['state_name'])

    df_income['outbound_migration'] = df_sum['outbound_migration']
    return df_income


def calculateCorrelation(df):
    df_income_sim = df.iloc[:,3:]
    corr = df_income_sim.corr()
    return corr
