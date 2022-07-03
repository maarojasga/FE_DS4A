import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import plotly.express as px

def app():
    plt.style.use('ggplot')
    plt.style.use('dark_background')
    color_discrete_map = {'geophony': '#2E75B6', "biophony": '#A9D18E', 'anthrophony': '#FFD966',"Other":"#F4B183"}
    df = pd.read_csv('data/Labeled Metatabla.csv')
    df['date'] = pd.to_datetime(df['date'])
    
    def mapa(df):
        fig2 = px.scatter_mapbox(df, lat="decimalLat", lon="decimalLon", hover_name="sensor_name", 
                        hover_data=["grand_label", "BI","NP","ACI","NDSI","ADI","H","Ht","Hf","SC"],
                        color_discrete_map=color_discrete_map,color="grand_label", zoom=9, width=800,height=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c2.plotly_chart(fig2)

    def filter_date(df, initial_date, final_date):
        update()
        
        if initial_date>final_date: return df

        df_filter = df[df['date'].dt.date >= initial_date]
        df_filter = df_filter[df['date'].dt.date <= final_date]
        
        return df_filter
    
    def filter_hour(df, start_hr, end_hr):
        update()

        df_filter = df[df['hour']>=start_hr]
        df_filter = df_filter[df_filter['hour']<=end_hr]

        return df_filter


    @st.cache
    def read_data():
        df = pd.read_csv('data/Labeled Metatabla.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df

    def transf_bio():
        df_bio = df[df['grand_label'] == 'biophony'] 
        print(df_bio.head())
        update()
        return df_bio

    def transf_antro():
        df_antro = df[df['grand_label'] == 'anthrophony']
        update() 
        return df_antro
    
    def transf_other():
        df_other = df[df['grand_label'] == 'Other']
        update() 
        return df_other

    def transf_geo():
        df_geo = df[df['grand_label'] == 'geophony']
        update() 
        return df_geo

    def update():
        update = True


    c1, c2= st.columns([1, 3])
    #column 1 config
    c1.write('### Date select')
    initial_date = c1.date_input('Start date', datetime.date(2021, 11, 1))
    final_date = c1.date_input('End date', datetime.date(2021, 12, 30))

    c1.write('### Time select')
    hr = list(range(24))
    start_hr, end_hr = c1.select_slider('Time', options=hr, value=[0,23])
    c1.write('### Category')
    tipo = c1.radio( 'Label', ['All']+list(set(df['grand_label'])))

    with st.spinner('Processing...'):
       df = read_data()

       df = filter_date(df, initial_date, final_date)

       df = filter_hour(df, start_hr, end_hr)

       df_bio = transf_bio()
       df_antro = transf_antro()
       df_other = transf_other()
       df_geo = transf_geo()
 

    st.write('--------------')

    if update:

        if tipo == 'biophony':
            mapa(df_bio)
        elif tipo == 'anthrophony':
            mapa(df_antro)
        elif tipo == 'geophony':
            mapa(df_geo)
        elif tipo == 'Other':
            mapa(df_other)
        else:
            mapa(df)