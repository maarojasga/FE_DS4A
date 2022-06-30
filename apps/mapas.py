import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import plotly.express as px

def app():
    plt.style.use('ggplot')
    plt.style.use('dark_background')
    #colors={:"green","":"purple","Anthro"}
    color_discrete_map = {'geophony': '#2E75B6', "biophony": '#A9D18E', 'anthrophony': '#FFD966',"Other":"#F4B183"}
    df = pd.read_csv('data/Labeled Metatabla.csv')
    df['date'] = pd.to_datetime(df['date'])

    def mapa(df):
        fig2 = px.scatter_mapbox(df, lat="decimalLat", lon="decimalLon", hover_name="sensor_name", hover_data=["grand_label", "time"],
                        color_discrete_map=color_discrete_map,color="grand_label", zoom=9, width=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    @st.cache
    def leer_data():
        return df

    def transf_bio():
        df_bio = df[df['grand_label'] == 'biophony'] 
        print(df_bio.head())
        return df_bio

    def transf_antro():
        df_antro = df[df['grand_label'] == 'anthrophony'] 
        return df_antro
    
    def transf_other():
        df_other = df[df['grand_label'] == 'Other'] 
        return df_other

    def transf_geo():
        df_geo = df[df['grand_label'] == 'geophony'] 
        return df_geo

    with st.spinner('Processing...'):
       df = leer_data()
       df_bio = transf_bio()
       df_antro = transf_antro()
       df_other = transf_other()
       df_geo = transf_geo()



    st.write('# Filters')

    
    c1, c2, c3 = st.columns(3)
    c1.write('### Dates')
    fecha_inicial = c1.date_input('Start date', datetime.date(2021, 11, 1))
    fecha_final = c1.date_input('End date', datetime.date(2021, 12, 30))
    c2.write('### Category')
    tipo = c2.radio( 'Tipo', ['All']+list(set(df['grand_label'])))
    #c3.write('### Sensor')
    #sensor = c3.multiselect('Nombre del sensor', ['Seleccionar']+list(set(df['name'])))
    seguir = c1.checkbox('Filter')
    st.write('--------------')

    if seguir:
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
