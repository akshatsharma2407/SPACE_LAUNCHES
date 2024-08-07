import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

df = pd.read_csv('mission_launches.csv')

df.drop(columns=['Unnamed: 0','Unnamed: 0.1'],inplace=True)

df.drop_duplicates(inplace=True)


df['Company Country'] = df['Organisation'].map({
                                'CASC':'China',
                                'IAI':'Israel',
                                'VKS RF':'Russia',
                                'ISA':'Israel',
                                'KARI':'South Korea',
                                'AEB':'Brazil',
                                'ISRO':'India',
                                'IRGC':'Iran',
                                'CASIC':'China',
                                'KCST':'North Korea',
                                'ESA':'Europe',
                                'NASA':'USA',
                                'ISAS':'Japan',
                                'RVSN USSR':'USSR',
                                'ASI':'Italy',
                                'US Air Force':'USA',
                                'CNES':'France',
                                "Arm??e de l'Air":'France',
                                'US Navy':'USA',
                                'SpaceX': 'USA',
                                'Roscosmos': 'Russia',
                                'ULA': 'USA',
                                'JAXA': 'Japan',
                                'Northrop': 'USA',
                                'ExPace': 'China',
                                'Rocket Lab': 'New Zealand',
                                'Virgin Orbit': 'USA',
                                'MHI': 'Japan',
                                'Arianespace': 'France',
                                'Blue Origin': 'USA',
                                'Exos': 'USA',
                                'ILS': 'USA',
                                'i-Space': 'China',
                                'OneSpace': 'China',
                                'Landspace': 'China',
                                'Eurockot': 'Russia',
                                'Land Launch': 'Russia',
                                'Sandia': 'USA',
                                'Kosmotras': 'Russia',
                                'Khrunichev': 'Russia',
                                'Sea Launch': 'International (Sea Platform)',
                                'Boeing': 'USA',
                                'SRC': 'USA',
                                'MITT': 'Russia',
                                'Lockheed': 'USA',
                                'Starsem': 'France',
                                'EER': 'Russia',
                                'General Dynamics': 'USA',
                                'Martin Marietta': 'USA',
                                'Yuzhmash': 'Ukraine',
                                'Douglas': 'USA',
                                'CECLES': 'Argentina',
                                'RAE': 'Argentina',
                                'UT': 'Russia',
                                'OKB-586': 'Russia',
                                'AMBA': 'Argentina',
                            }).fillna('Private')

df['Organisation_type'] = df['Organisation'].apply(lambda x : 'PRVT' if x in ['SpaceX', 'ULA', 'Northrop', 'ExPace',
       'Rocket Lab', 'Virgin Orbit', 'MHI', 'Arianespace', 'Blue Origin',
       'Exos', 'ILS', 'i-Space', 'OneSpace', 'Landspace', 'Eurockot',
       'Land Launch', 'Kosmotras', 'Sea Launch',
       'Boeing', 'MITT', 'Lockheed', 'Starsem',
       'General Dynamics', 'Martin Marietta', 'Douglas',
       ] else 'GOVT')


df['Date'] = df['Date'].apply(lambda x:x[4:-4] if 'UTC' in x else x[4:] + ' 00:00')

df['date'] = pd.to_datetime(df['Date'],errors='coerce')

df.drop(columns='Date',inplace=True)

df['decades'] = (df['date'].dt.year // 10) * 10

def load_general_analysis():
     st.metric('LAUNCHED SATERLITE TILL 2020',df.shape[0])
     
     #NUMBER OF LAUNCHES BY COUNTRY
     st.subheader('NUMBER OF LAUNCHES PER COUNTRY')
     countryWiseLaunch = df.groupby('Company Country')['Detail'].count()
     fig5, ax5 = plt.subplots()
     ax5.bar(countryWiseLaunch.index, countryWiseLaunch.values)
     plt.xticks(rotation=45, ha='right')
     ax5.set_xlabel('Country')
     ax5.set_ylabel('Number of Launches')
     ax5.set_title('Number of Launches by Country')
     st.pyplot(fig5)

     #NUMBER OF LAUNCHES BY DECADES
     st.subheader('NUMBER OF LAUNCHES PER DECADES')
     decadesWiseLaunch = df.groupby('decades')['Detail'].count()
     fig5, ax5 = plt.subplots()
     ax5.bar(decadesWiseLaunch.index, decadesWiseLaunch.values)
     plt.xticks(rotation=45, ha='right')
     ax5.set_xlabel('DECADES')
     ax5.set_ylabel('Number of Launches')
     ax5.set_title('Number of Launches by decades')
     st.pyplot(fig5)

     #STATUSRETIRED VS ACTIVE
     st.subheader('RETIRED VS ACTIVE')
     status = df.groupby('Rocket_Status')['Detail'].count()
     fig6,ax6 = plt.subplots()
     ax6.pie(status,labels = status.index,autopct='%0.01f%%',startangle=90)
     ax6.axis('equal')
     st.pyplot(fig6)

     #SUCCESS VS FAILURE
     st.subheader('SUCCESS VS FAILURE')
     mission = df.groupby('Mission_Status')['Detail'].count()
     fig7,ax7 = plt.subplots()
     ax7.pie(mission,labels = mission.index,autopct='%0.01f%%',startangle=90)
     ax7.axis('equal')
     st.pyplot(fig7)


def load_first_mission(selected_country):
        x = df[df['Company Country'] == selected_country]['date'].min()
        values = df[(df['Company Country'] == selected_country) & (df['date'] == x)].values[0]
        # print(values)
        st.metric('Mission Name',values[2])
        st.metric('Launched by',values[-4])
        st.metric('Space Agency Name',values[0])
        st.metric('Location of Launch',values[1])
        st.metric('Date',str(values[-2]))
        st.metric('OUTCOME',values[-5])
        st.metric('STATUS',values[-7])

def countryAllMissions(selected_country):
     allsatellite = df[df['Company Country'] == selected_country]
     st.dataframe(allsatellite)

     col1,col2 = st.columns(2)
     with col1:
        st.subheader('ACTIVE vs RETIRED')
        plot = allsatellite['Rocket_Status'].value_counts()
        fig,ax = plt.subplots()
        ax.pie(plot,labels = plot.index,autopct='%0.01f%%')
        st.pyplot(fig)

        st.subheader('TOP YEARS WHERE MOST SATELLITE ARE LAUNCHED')
        plot = allsatellite['date'].dt.year.value_counts().head(10)
        fig3,ax3 = plt.subplots()
        ax3.pie(plot,labels = plot.index,autopct='%0.01f%%',startangle=90)
        ax.axis('equal')
        st.pyplot(fig3)

     with col2:
        st.subheader('ORGANISATIONS')
        plot = allsatellite['Organisation'].value_counts()
        fig1,ax1 = plt.subplots()
        ax1.pie(plot,labels = plot.index,autopct='%0.01f%%')
        st.pyplot(fig1)

        st.subheader('SUCCESS vs FAILURE')
        plot = allsatellite['Mission_Status'].value_counts()
        fig4,ax4 = plt.subplots()
        ax4.pie(plot,labels = plot.index,autopct='%0.01f%%')
        st.pyplot(fig4)
     
     st.subheader('LOCATIONS')
     plot = allsatellite['Location'].value_counts()
     fig2,ax2 = plt.subplots()
     ax2.pie(plot,labels = plot.index,autopct='%0.01f%%')
     st.pyplot(fig2)

def perticular_mission(selected_mission):
        values = df[df['Detail'] == selected_mission].values[0]
        print(values)
        st.metric('Mission Name',values[2])
        st.metric('Launched by',values[-4])
        st.metric('Space Agency Name',values[0])
        st.metric('Location of Launch',values[1])
        st.metric('Date',str(values[-2]))
        st.metric('OUTCOME',values[-5])
        st.metric('STATUS',values[-7])

def org1vsorg2(org1,org2):

     st.title(f'A DETAIL COMPARISON BETWEEN {org1} AND {org2}')
     col1,col2 = st.columns(2)
     with col1:
     #ORGANISATION TYPE
          st.metric(f'ORGANISATION TYPE of {org1}',df[df['Organisation'] == org1]['Organisation_type'].values[0])
     #COUNTRY
          st.metric(f'COUNTRY/PLACE OF ORIGIN {org1}',df[df['Organisation'] == org1]['Company Country'].values[0])
     #COUNT OF LAUCHES
          st.metric(f'NUMBER OF LAUNCHES BY {org1}',df[df['Organisation'] == org1].shape[0])
     #PLOT OF SUCCESS VS FAILURE
          try:
            success = int(df[df['Organisation'] == org1].groupby('Mission_Status')['Mission_Status'].value_counts()['Success'])
            st.metric(f'SUCCESSFULL LAUNCHES BY {org1}',success,success)
          except:
            st.metric(f'SUCCESSFULL LAUNCHES BY {org1}', 0,0)

          try:
            fail = int(df[df['Organisation'] == org1].groupby('Mission_Status')['Mission_Status'].value_counts()['Failure'])
            st.metric(f'FAILED LAUNCHES BY {org1}', fail,-(fail))
          except:
            st.metric(f'FAILED LAUNCHES BY {org1}', 0,-(0))
          
          try:
            partialfailure = int(df[df['Organisation'] == org1].groupby('Mission_Status')['Mission_Status'].value_counts()['Partial Failure'])
            st.metric(f'Partial Failure LAUNCHES BY {org1}', partialfailure,partialfailure)
          except:
            st.metric(f'Partial Failure LAUNCHES BY {org1}', 0,(0))
          
          try:
            prelaunch = int(df[df['Organisation'] == org1].groupby('Mission_Status')['Mission_Status'].value_counts()['Prelaunch Failure'])
            st.metric(f'PRE LAUNCH Failure LAUNCHES BY {org1}', prelaunch,-(prelaunch))
          except:
            st.metric(f'PRE LAUNCH Failure LAUNCHES BY {org1}', 0,-0)
              
     #RETIRED VS ACTIVE
          try:
            active = int(df[df['Organisation'] == org1].groupby('Rocket_Status')['Rocket_Status'].value_counts()['StatusActive'])
            st.metric(f'ACTIVE SATELLITE BY {org1}',active,active)
          except:
            st.metric(f'ACTIVE SATELLITE BY {org1}', 0,0)

          try:
            retired = int(df[df['Organisation'] == org1].groupby('Rocket_Status')['Rocket_Status'].value_counts()['StatusRetired'])
            st.metric(f'RETIRED SATELLITE BY {org1}', retired,-(retired))
          except:
            st.metric(f'RETIRED SATELLITE BY {org1}', 0,-(0))
              
     #DATAFRAME OF ALL LAUNCHES
          st.dataframe(df[df['Organisation'] == org1])
     
     # #PLOT OF SUCCESS VS FAILURE
     #      plot1 = df[df['Organisation'] == org2].groupby('Mission_Status')['Mission_Status'].value_counts()
     #      fig1,ax1 = plt.subplots()
     #      ax1.pie(plot1,labels = plot2.index,autopct='%0.01f%%')
     #      ax1.set_title(f'SUCCESS VS FAILURE OF LAUCHES OF {org1}')
     #      st.pyplot(fig1)


     with col2:
     #ORGANISATION TYPE
          st.metric(f'ORGANISATION TYPE of {org2}',df[df['Organisation'] == org2]['Organisation_type'].values[0])
     #COUNTRY
          st.metric(f'COUNTRY/PLACE OF ORIGIN {org2}',df[df['Organisation'] == org2]['Company Country'].values[0])
     #COUNT OF LAUCHES
          st.metric(f'NUMBER OF LAUNCHES BY {org2}',df[df['Organisation'] == org2].shape[0])
     #PLOT OF SUCCESS VS FAILURE
          try:
            success = int(df[df['Organisation'] == org2].groupby('Mission_Status')['Mission_Status'].value_counts()['Success'])
            st.metric(f'SUCCESSFULL LAUNCHES BY {org2}',success,success)
          except:
            st.metric(f'SUCCESSFULL LAUNCHES BY {org2}', 0,0)

          try:
            fail = int(df[df['Organisation'] == org2].groupby('Mission_Status')['Mission_Status'].value_counts()['Failure'])
            st.metric(f'FAILED LAUNCHES BY {org2}', fail,-(fail))
          except:
            st.metric(f'FAILED LAUNCHES BY {org2}', 0,-(0))
          
          try:
            partialfailure = int(df[df['Organisation'] == org2].groupby('Mission_Status')['Mission_Status'].value_counts()['Partial Failure'])
            st.metric(f'Partial Failure LAUNCHES BY {org2}', partialfailure,partialfailure)
          except:
            st.metric(f'Partial Failure LAUNCHES BY {org2}', 0,(0))
          
          try:
            prelaunch = int(df[df['Organisation'] == org2].groupby('Mission_Status')['Mission_Status'].value_counts()['Prelaunch Failure'])
            st.metric(f'PRE LAUNCH Failure LAUNCHES BY {org2}', prelaunch,-(prelaunch))
          except:
            st.metric(f'PRE LAUNCH Failure LAUNCHES BY {org2}', 0,-0)
     
     #RETIRED VS ACTIVE
          try:
            active = int(df[df['Organisation'] == org2].groupby('Rocket_Status')['Rocket_Status'].value_counts()['StatusActive'])
            st.metric(f'ACTIVE SATELLITE BY {org2}',active,active)
          except:
            st.metric(f'ACTIVE SATELLITE BY {org2}', 0,0)

          try:
            retired = int(df[df['Organisation'] == org2].groupby('Rocket_Status')['Rocket_Status'].value_counts()['StatusRetired'])
            st.metric(f'RETIRED SATELLITE BY {org2}', retired,-(retired))
          except:
            st.metric(f'RETIRED SATELLITE BY {org2}', 0,-(0))

     #DATAFRAME OF ALL LAUNCHES
          st.dataframe(df[df['Organisation'] == org2])
     # #PLOT OF SUCCESS VS FAILURE
     #      plot2 = df[df['Organisation'] == org2].groupby('Mission_Status')['Mission_Status'].value_counts()
     #      fig2,ax2 = plt.subplots()
     #      ax2.pie(plot2,labels = plot2.index,autopct='%0.01f%%')
     #      ax2.set_title(f'SUCCESS VS FAILURE OF LAUCHES OF {org2}')
     #      st.pyplot(fig2)

     #redefine col1,col2 for having a title 

st.sidebar.title('SPACE ANALYSIS')
option = st.sidebar.selectbox('Select One',['GENERAL ANALYSIS','FIRST MISSION OF COUNTRY','ALL MISSION OF A COUNTRY','PERTICULAR MISSION','ORGANISATION VS ORGANISATION'])

if option == 'GENERAL ANALYSIS':
     load_general_analysis()

elif option == 'FIRST MISSION OF COUNTRY':
    selected_country = st.sidebar.selectbox('SELECT COUNTRY',sorted(df['Company Country'].unique()))
    btn = st.sidebar.button('Select')
    if btn:
        load_first_mission(selected_country)


elif option == 'ALL MISSION OF A COUNTRY':
    selected_country = st.sidebar.selectbox('SELECT COUNTRY',sorted(df['Company Country'].unique()))
    btn = st.sidebar.button('Select')
    if btn:
         countryAllMissions(selected_country)

elif option == 'PERTICULAR MISSION':
     selected_mission = st.sidebar.selectbox('SELECT MISSION',sorted(df['Detail'].unique()))
     btn = st.sidebar.button('Select')
     if btn:
          perticular_mission(selected_mission)

elif option == 'ORGANISATION VS ORGANISATION':
     org1 = st.sidebar.selectbox('SELECT FIRST ORGANISATION',sorted(df['Organisation'].unique()))
     org2 = st.sidebar.selectbox('SELECT SECOND ORGANISATION',sorted(df['Organisation'].unique()))
     btn = st.sidebar.button('Select')
     if btn:
          org1vsorg2(org1,org2)
