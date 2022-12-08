import pandas as pd

def get_income_df():
    df_sum = pd.read_csv("data/state_migration.csv")

    df_d = df_sum.groupby(['d_state_name']).agg({'n':'sum'})
    df_d = df_d.reset_index()
    df_income = pd.read_csv("data/state_household_income.csv")

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
