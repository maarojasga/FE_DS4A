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
    color_discrete_map = {'Geophony': '#2E75B6', "Biophony": '#A9D18E', 'Anthrophony': '#FFD966',"Other":"#F4B183"}

    def mapa():
        fig2 = px.scatter_mapbox(df, lat="latitud", lon="longitud", hover_name="sensor_name", hover_data=["parent label", "time"],
                        color_discrete_map=color_discrete_map,color="parent label", zoom=9, width=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    def mapa_bio():
        fig2 = px.scatter_mapbox(df_bio, lat="latitud", lon="longitud", hover_name="sensor_name", hover_data=["parent label", "parent label"],
                        color_discrete_map=color_discrete_map,color="parent label", zoom=9, width=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    def mapa_antro():
        fig2 = px.scatter_mapbox(df_antro, lat="latitud", lon="longitud", hover_name="sensor_name", hover_data=["parent label", "parent label"],
                        color_discrete_map=color_discrete_map, color="parent label", zoom=9, width=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    def mapa_other():
        fig2 = px.scatter_mapbox(df_other, lat="latitud", lon="longitud", hover_name="sensor_name", hover_data=["parent label", "parent label"],
                        color_discrete_map=color_discrete_map,color="parent label", zoom=9, width=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    def mapa_geo():
        fig2 = px.scatter_mapbox(df_geo, lat="latitud", lon="longitud", hover_name="sensor_name", hover_data=["parent label", "parent label"],
                        color_discrete_map=color_discrete_map, color="parent label", zoom=9, width=800)
        fig2.update_layout(mapbox_style="open-street-map")

        fig2.update_layout(margin={"r":0,"t":50,"l":0,"b":50})

        fig2.update_coloraxes(showscale=False)
        c1.plotly_chart(fig2)

    @st.cache
    def leer_data():
        df = pd.read_csv('data/FrontEnd_Part1.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df

    def transf_bio():
        df = pd.read_csv('data/FrontEnd_Part1.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df_bio = df[df['parent label'] == 'Biophony'] 
        return df_bio

    def transf_antro():
        df = pd.read_csv('data/FrontEnd_Part1.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df_antro = df[df['parent label'] == 'Anthrophony'] 
        return df_antro
    
    def transf_other():
        df = pd.read_csv('data/FrontEnd_Part1.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df_other = df[df['parent label'] == 'Other'] 
        return df_other

    def transf_geo():
        df = pd.read_csv('data/FrontEnd_Part1.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        df_geo = df[df['parent label'] == 'Geophony'] 
        return df_geo

    with st.spinner('En proceso...'):
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
    tipo = c2.radio( 'Tipo', ['All']+list(set(df['parent label'])))
    #c3.write('### Sensor')
    #sensor = c3.multiselect('Nombre del sensor', ['Seleccionar']+list(set(df['name'])))
    seguir = c1.checkbox('Filter')
    st.write('--------------')

    if seguir:
        if tipo == 'Biophony':
            mapa_bio()
        elif tipo == 'Anthrophony':
            mapa_antro()
        elif tipo == 'Geophony':
            mapa_geo()
        elif tipo == 'Other':
            mapa_other()
        else:
            mapa()
        
        #totales = data.sum()
