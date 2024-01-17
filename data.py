import pandas as pd

df = pd.read_csv('C:/olympic/athlete_events.csv')
region = pd.read_csv('C:/olympic/noc_regions.csv')
dg = pd.read_csv('C:/tokyo/2020_Olympics_Dataset.csv', encoding='latin-1')


def preprocessor(df, region, dg):


    df = df.drop(['Height', 'Weight', 'ID'], axis=1)   #for columns drop
    df = df[df['Season'] == 'Summer']  #to filter the data
    dg.rename(columns={'Gender': 'Sex', 'Country': 'Team'}, inplace=True)   # for rename the columns

    #add the new columns
    dg['Season'] = dg['Season'] = "Summer"
    dg['Games'] = dg['Games'] = "2020 Summer"
    dg['Year'] = dg['Year'] = 2020
    dg['City'] = dg['City'] = 'Tokyo'
    #column drop
    dg = dg.drop(['Unnamed: 0', 'Discipline', 'Rank', 'Code'], axis=1)
    #for relocate the columns
    dg = dg.iloc[:, [0, 1, 2, 4, 3, 9, 10, 8, 11, 5, 6, 7]]
    #for replace the name
    dg['Sex'] = dg['Sex'].replace(['Male'], 'M')
    dg['Sex'] = dg['Sex'].replace(['Female'], 'F')
    #to merge the data or append the data
    df = pd.concat([df, dg], axis=0)
    #add new data in the datasets
    new = pd.DataFrame({'NOC': 'ROC', 'region': 'Russia', 'notes': 'NaN'}, index=[167])
    region = pd.concat([new, region.loc[:]]).reset_index(drop=True)
    new = pd.DataFrame({'NOC': 'SGP', 'region': 'Singapore', 'notes': 'NaN'}, index=[178])
    region = pd.concat([new, region.loc[:]]).reset_index(drop=True)
    new = pd.DataFrame({'NOC': 'LBN', 'region': 'Lebanon', 'notes': 'NaN'}, index=[120])
    region = pd.concat([new, region.loc[:]]).reset_index(drop=True)
    new = pd.DataFrame({'NOC': 'EOR', 'region': 'Refugee', 'notes': 'NaN'}, index=[48])
    #add the dataframe from the above
    region = pd.concat([new, region.loc[:]]).reset_index(drop=True)
    #merge the data
    df = df.merge(region, on='NOC', how='left')
    df.drop_duplicates(inplace=True)
    medals = pd.get_dummies(df['Medal'])
    df = pd.concat([df, medals], axis=1)

    return df

