import pandas as pd
import numpy as np

def winter_medal_tally(dl,years,country):
    medal_df = dl.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal', 'region'])
    flag = 0
    if years == 'Overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'Overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'Overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == years]
    if years != 'Overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == years) & (medal_df['region'] == country)]
    if flag == 1:

        a = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Year',
                                                                                    ascending=True).reset_index()

    else:
        a = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    a['Total'] = a['Gold'] + a['Silver'] + a['Bronze']

    return a
def medal_tally_winter(dl):

    medal_tally = dl.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal', 'region'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',ascending=False).reset_index()
    medal_tally = medal_tally.replace([1074, 843, 197, 300, 338, 322], [1063, 832, 199, 284, 318, 314])
    medal_tally['Total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally.rename(columns={'region': 'Country'}, inplace=True)

    return medal_tally

def country_list(dl):

    years = dl['Year'].unique().tolist()
    years.sort()
    years.insert(0, 'Overall')

    country = np.unique(dl['region'].dropna().values).tolist()
    country.sort()
    country.insert(0, 'Overall')

    return years,country


def winter_over_nation_parts(dl):
    nation_parts = dl.drop_duplicates(['Year', 'region'])['Year'].value_counts().reset_index()
    nation_parts = nation_parts.sort_values('index')
    nation_parts.rename(columns={'index': 'Editions', 'Year': 'No. of Countries'}, inplace=True)
    return nation_parts

def winter_over_events(dl):
    events_part = dl.drop_duplicates(['Year', 'Event'])['Year'].value_counts().reset_index()
    events_part.rename(columns={'index': 'Year', 'Year': 'No. of events'}, inplace=True)
    events_part=events_part.sort_values('Year')
    return events_part

def winter_over_athletes(dl):
    athletes_part = dl.drop_duplicates(['Year', 'Name'])['Year'].value_counts().reset_index()
    athletes_part.rename(columns={'index': 'Year', 'Year': 'No. of Athletes'}, inplace=True)
    athletes_part=athletes_part.sort_values('Year')
    return athletes_part


def winter_most_successful(dl, sport):
    temp_df = dl.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df['Name'].value_counts().reset_index().head(15).merge(dl, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals', 'region': 'Country'}, inplace=True)
    return x


def winter_country_tally(dl,country):
    temp = dl.dropna(subset='Medal')
    temp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)
    new_temp = temp[temp['region'] == country]
    f_temp = new_temp.groupby('Year').count()['Medal'].reset_index()

    return f_temp



def winter_country_heatmap(dl,country):
    temp = dl.dropna(subset='Medal')
    temp.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_temp = temp[temp['region'] == country]





    return new_temp


def winter_most_successful_ath(dl, country):
    temp_df = dl.dropna(subset=['Medal'])

    temp_df = temp_df[temp_df['region'] == country]

    x = temp_df['Name'].value_counts().reset_index().head(10).merge(dl, left_on='index', right_on='Name', how='left')[
        ['index', 'Name_x', 'Sport', 'region']].drop_duplicates('index')
    x.rename(columns={'index': 'Name', 'Name_x': 'Medals', 'region': 'Country'}, inplace=True)

    return x


def winter_men_vs_female(dl):
    m = dl[dl['Sex'] == 'M'].groupby('Year').count()['Name'].reset_index()
    f = dl[dl['Sex'] == 'F'].groupby('Year').count()['Name'].reset_index()
    final = m.merge(f, on='Year', how='left')
    final.rename(columns={'Name_x': 'Male', 'Name_y': 'Female'}, inplace=True)
    final.fillna(0, inplace=True)

    return final