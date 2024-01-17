import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np
import plotly.figure_factory as ff
import seaborn as sb
from PIL import Image
import data, page
import winter,winterpage

df = pd.read_csv('C:/olympic/athlete_events.csv')
region = pd.read_csv('C:/olympic/noc_regions.csv')
dg = pd.read_csv('C:/tokyo/2020_Olympics_Dataset.csv', encoding='latin-1')
season=st.sidebar.selectbox('Choose Season',('Summer','Winter'))
df=data.preprocessor(df,region,dg)
dl = pd.read_csv('C:/olympic/athlete_events.csv')
region_dl = pd.read_csv('C:/olympic/noc_regions.csv')
dl=winter.winter_df(dl,region_dl)


st.sidebar.image('https://www.pngall.com/wp-content/uploads/10/Olympics-Silhouette-PNG-Image.png')

if season =='Summer':
    st.sidebar.title('Olympics 124 years Analysis')
    user_menu = st.sidebar.radio(
        'Select an option',
        ('Medal Tally', 'Overall Analysis', 'Country_wise Analysis', 'Athlete Wise Analysis')
    )
    if user_menu == 'Medal Tally':
        st.sidebar.header('Medal_Tally')
        years, country = page.country_list(df)
        select_year = st.sidebar.selectbox("Select Year", years)
        select_country = st.sidebar.selectbox("Select Country", country)
        if select_year=='Overall' and select_country =='Overall':
            st.title('Overall medal Tally')

        if select_year != 'Overall' and select_country == 'Overall':
            st.title("overall Medal tally in " +  str(select_year))

        if select_year == 'Overall' and select_country != 'Overall':
            st.title(str(select_country)  + ' Medal Tally')

        if select_year != 'Overall' and select_country != 'Overall':
            st.title(str(select_country) + ' Medal Tally In ' + str(select_year ))

        medal_tally = page.get_medal_tally(df, select_year, select_country)
        medal_tally=medal_tally.rename(columns={'region': 'Country'})
        st.table(medal_tally)

    if user_menu=='Overall Analysis':
        editions=df['Year'].unique().shape[0] - 1
        cities=df['City'].unique().shape[0]
        sports=df['Sport'].unique().shape[0]
        events=df['Event'].unique().shape[0]
        nation=df['region'].unique().shape[0]
        athletes=df['Name'].unique().shape[0]
        st.title('Overall Statistics')
        col1,col2,col3=st.columns(3)
        with col1:
            st.subheader("Editions")
            st.header(editions)
        with col2:
            st.subheader("**Hosts**")
            st.header(cities)

        with col3:
            st.subheader("Games")
            st.header(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Countries")
            st.header(nation)
        with col2:
            st.subheader("Events")
            st.header(events)

        with col3:
            st.subheader("Athletes")
            st.header(athletes)


        nation_parts=page.over_nation_parts(df)
        fig = px.line(nation_parts, x='Editions', y='No. of Countries')
        st.title('Participating Countries Over The Years')
        st.plotly_chart(fig)

        events_part=page.over_events(df)
        figu = px.line(events_part, x='Year', y='No. of events')
        st.title('No. of Events Over The Years')
        st.plotly_chart(figu)

        athletes_part = page.over_athletes(df)
        figur = px.line(athletes_part, x='Year', y='No. of Athletes')
        st.title('No. of Athletes Over The Years')
        st.plotly_chart(figur)

        st.title('No. Of Events Over Time(Every Sport)')
        fig,ax=plt.subplots(figsize=(20,20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax=sb.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)


        st.title('Successfull Atheletes')
        sport_list=df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')
        selected_sport=st.selectbox('Select a Sport' , sport_list)
        x=page.most_successful(df,selected_sport)
        st.table(x)
    if user_menu=='Country_wise Analysis':
        country_list = np.unique(df['region'].dropna().values).tolist()
        country_list.sort()
        country_list.insert(0, 'Overall')
        country_select=st.sidebar.selectbox('Select a country', country_list)
        f_temp=page.country_tally(df,country_select)

        figu = px.line(f_temp, x='Year', y='Medal')
        st.title(country_select + ' medal tally over the years')
        st.plotly_chart(figu)

        #st.title(country_select + ' performance over the sports')
        #new_temp=page.country_heatmap(df,country_select)
        #fig,x=plt.subplots(figsize=(20, 20))
        #x=sb.heatmap(new_temp.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int'),annot=True)
        #st.pyplot(fig)
        st.title('Top 10 Athletes of '+ country_select)
        top_df=page.most_successful_ath(df,country_select)
        st.table(top_df)


    if user_menu == 'Athlete Wise Analysis':
        athlete_df = df.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                 show_hist=False, show_rug=False)

        st.title('Distribution of age')
        st.plotly_chart(fig)

        x=[]
        name=[]
        famous_sports =['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
       'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
       'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
       'Water Polo', 'Hockey', 'Rowing', 'Fencing',
       'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
       'Tennis',  'Golf', 'Softball', 'Archery',
       'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
       'Rhythmic Gymnastics', 'Rugby Sevens',
       'Beach Volleyball',  'Rugby', 'Lacrosse', 'Ice Hockey','Karate', ]
        for sport in famous_sports:
            temp_df =athlete_df[athlete_df['Sport']==sport]
            x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x,name, show_hist=False, show_rug=False)

        st.title('Distribution of age wrt sports(Gold Medalist)')
        st.plotly_chart(fig)

        x = []
        name = []
        famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                         'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                         'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                         'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                         'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                         'Tennis', 'Golf', 'Softball', 'Archery',
                         'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                         'Rhythmic Gymnastics', 'Rugby Sevens',
                         'Beach Volleyball', 'Rugby', 'Lacrosse', 'Ice Hockey', 'Karate', ]
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

        st.title('Distribution of age wrt sports(Silver Medalist)')
        st.plotly_chart(fig)

        x = []
        famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                         'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                         'Art Competitions', 'Handball', 'Weightlifting']


        name = []
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

        st.title('Distribution of age wrt sports(Bronze Medalist)')
        st.plotly_chart(fig)

        st.title('Male & Female Participation')
        final=page.men_vs_female(df)
        fig = px.line(final, x='Year', y=['Male', 'Female'])
        st.plotly_chart(fig)

if season =='Winter':
    st.sidebar.title('Olympics 90 years Analysis')
    user_menu = st.sidebar.radio(
        'Select an option',
        ('Medal Tally', 'Overall Analysis', 'Country_wise Analysis', 'Athlete Wise Analysis')
    )
    if user_menu == 'Medal Tally':
        st.sidebar.header('Medal_Tally')
        years, country = winterpage.country_list(dl)
        select_year = st.sidebar.selectbox("Select Year", years)
        select_country = st.sidebar.selectbox("Select Year", country)
        medal_tally = winterpage.winter_medal_tally(dl, select_year, select_country)
        st.table(medal_tally)


    if user_menu=='Overall Analysis':
        editions=dl['Year'].unique().shape[0] - 1
        cities=dl['City'].unique().shape[0]
        sports=dl['Sport'].unique().shape[0]
        events=dl['Event'].unique().shape[0]
        nation=dl['region'].unique().shape[0]
        athletes=dl['Name'].unique().shape[0]
        st.title('Overall Statistics')
        col1,col2,col3=st.columns(3)
        with col1:
            st.subheader("Editions")
            st.header(editions)
        with col2:
            st.subheader("**Hosts**")
            st.header(cities)

        with col3:
            st.subheader("Games")
            st.header(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.subheader("Countries")
            st.header(nation)
        with col2:
            st.subheader("Events")
            st.header(events)

        with col3:
            st.subheader("Athletes")
            st.header(athletes)


        nation_parts=winterpage.winter_over_nation_parts(dl)
        fig = px.line(nation_parts, x='Editions', y='No. of Countries')
        st.title('Participating Countries Over The Years')
        st.plotly_chart(fig)

        events_part=winterpage.winter_over_events(dl)
        figu = px.line(events_part, x='Year', y='No. of events')
        st.title('No. of Events Over The Years')
        st.plotly_chart(figu)

        athletes_part = winterpage.winter_over_athletes(dl)
        figur = px.line(athletes_part, x='Year', y='No. of Athletes')
        st.title('No. of Athletes Over The Years')
        st.plotly_chart(figur)

        st.title('No. Of Events Over Time(Every Sport)')
        fig,ax=plt.subplots(figsize=(20,20))
        x = dl.drop_duplicates(['Year', 'Sport', 'Event'])
        ax=sb.heatmap(x.pivot_table(index='Sport',columns='Year',values='Event',aggfunc='count').fillna(0).astype('int'),annot=True)
        st.pyplot(fig)


        st.title('Successfull Atheletes')
        sport_list=dl['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')
        selected_sport=st.selectbox('Select a Sport' , sport_list)
        x=winterpage.winter_most_successful(dl,selected_sport)
        st.table(x)

    if user_menu=='Country_wise Analysis':
        country_list = np.unique(dl['region'].dropna().values).tolist()
        country_list.sort()
        country_list.insert(0, 'Select')
        country_select=st.sidebar.selectbox('Select a country', country_list)
        f_temp=winterpage.winter_country_tally(df,country_select)

        figu = px.line(f_temp, x='Year', y='Medal')
        st.title(country_select + ' medal tally over the years')
        st.plotly_chart(figu)

        #st.title(country_select + ' performance over the sports')
        #new_temp=page.country_heatmap(df,country_select)
        #fig,x=plt.subplots(figsize=(20, 20))
        #x=sb.heatmap(new_temp.pivot_table(index='Sport',columns='Year',values='Medal',aggfunc='count').fillna(0).astype('int'),annot=True)
        #st.pyplot(fig)
        st.title('Top 10 Athletes of '+ country_select)
        top_df=winterpage.winter_most_successful_ath(df,country_select)
        st.table(top_df)

    if user_menu == 'Athlete Wise Analysis':
        athlete_df = dl.drop_duplicates(subset=['Name', 'region'])
        x1 = athlete_df['Age'].dropna()
        x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
        x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
        x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

        fig = ff.create_distplot([x1, x2, x3, x4],
                                 ['Overall age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],
                                 show_hist=False, show_rug=False)

        st.title('Distribution of age')
        st.plotly_chart(fig)

        x=[]
        name=[]
        famous_sports =['Speed Skating', 'Cross Country Skiing', 'Ice Hockey', 'Biathlon',
       'Alpine Skiing', 'Luge', 'Bobsleigh', 'Figure Skating',
       'Nordic Combined', 'Freestyle Skiing', 'Ski Jumping', 'Curling',
       'Snowboarding', 'Short Track Speed Skating', 'Skeleton',
       'Military Ski Patrol', 'Alpinism']
        for sport in famous_sports:
            temp_df =athlete_df[athlete_df['Sport']==sport]
            x.append(temp_df[temp_df['Medal']=='Gold']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x,name, show_hist=False, show_rug=False)

        st.title('Distribution of age wrt sports(Gold Medalist)')
        st.plotly_chart(fig)

        x = []
        name = []
        famous_sports = ['Speed Skating', 'Cross Country Skiing', 'Ice Hockey', 'Biathlon',
       'Alpine Skiing', 'Luge', 'Bobsleigh', 'Figure Skating',
       'Nordic Combined', 'Freestyle Skiing', 'Ski Jumping', 'Curling',
       'Snowboarding']
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Silver']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

        st.title('Distribution of age wrt sports(Silver Medalist)')
        st.plotly_chart(fig)

        x = []
        famous_sports = ['Speed Skating', 'Cross Country Skiing', 'Ice Hockey', 'Biathlon',
       'Alpine Skiing', 'Luge', 'Bobsleigh', 'Figure Skating',
       'Nordic Combined', 'Freestyle Skiing', 'Ski Jumping', 'Curling',
       'Snowboarding']


        name = []
        for sport in famous_sports:
            temp_df = athlete_df[athlete_df['Sport'] == sport]
            x.append(temp_df[temp_df['Medal'] == 'Bronze']['Age'].dropna())
            name.append(sport)

        fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)

        st.title('Distribution of age wrt sports(Bronze Medalist)')
        st.plotly_chart(fig)

        st.title('Male & Female Participation')
        final=winterpage.winter_men_vs_female(dl)
        fig = px.line(final, x='Year', y=['Male', 'Female'])
        st.plotly_chart(fig)





