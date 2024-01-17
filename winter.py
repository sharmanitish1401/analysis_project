import pandas as pd

dl = pd.read_csv('C:/olympic/athlete_events.csv')
region_dl = pd.read_csv('C:/olympic/noc_regions.csv')

def winter_df(dl,region_dl):

    dl = dl.drop(columns=['Height', 'Weight', 'ID'], axis=1)
    dl = dl[dl['Season'] == 'Winter']
    new = pd.DataFrame({'NOC': 'ROC', 'region': 'Russia', 'notes': 'NaN'}, index=[167])
    region_dl = pd.concat([new, region_dl.loc[:]]).reset_index(drop=True)
    new = pd.DataFrame({'NOC': 'SGP', 'region': 'Singapore', 'notes': 'NaN'}, index=[178])
    region_dl = pd.concat([new, region_dl.loc[:]]).reset_index(drop=True)
    new = pd.DataFrame({'NOC': 'EOR', 'region': 'Refugee', 'notes': 'NaN'}, index=[48])
    region_dl = pd.concat([new, region_dl.loc[:]]).reset_index(drop=True)
    new = pd.DataFrame({'NOC': 'LBN', 'region': 'Lebanon', 'notes': 'NaN'}, index=[120])
    region_dl = pd.concat([new, region_dl.loc[:]]).reset_index(drop=True)
    dl = dl.merge(region_dl, on='NOC', how='left')
    dl['Medal'].value_counts()
    medals = pd.get_dummies(dl['Medal'])
    dl = pd.concat([dl, medals], axis=1)

    return dl
