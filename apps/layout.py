from cProfile import label
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import plotly.express as px

def app():


    plt.style.use('ggplot')
    plt.style.use('dark_background')

    def read_data():
        df = pd.read_csv('data/FrontEnd_Part1.csv')
        df['Fecha'] = pd.to_datetime(df['Fecha'])
        return df

    def filter_parent_label(df, tipo):
        update()
        if tipo == 'Todos': return df
        else:
            df_filter = df[df['parent label'] == tipo]
            return df_filter

    def filter_date(df, initial_date, final_date):
        update()
        
        if initial_date>final_date: return df

        df_filter = df[df['Fecha'].dt.date >= initial_date]
        df_filter = df_filter[df['Fecha'].dt.date <= final_date]
        
        return df_filter
    
    def filter_hour(df, start_hr, end_hr):
        update()

        df_filter = df[df['hour']>=start_hr]
        df_filter = df_filter[df_filter['hour']<=end_hr]

        return df_filter

    def group_data(df, group_options):
        if group_options:
            df_filter = df.groupby(group_options).size()
            df_filter = pd.DataFrame(df_filter)
            df_filter.rename(columns = {0:'index'}, inplace = True)
            df_filter = df_filter.sort_values('index', ascending = False)
            return df_filter
        
        else: return df

    def linep(data):
        return st.line_chart(data)


    def barp(data):
        return st.bar_chart(data)

        
    def update():
        update = True






    df = read_data()
    df['date'] = df['Fecha'].dt.date #adding date column (temporal)





    #set columns
    c1, c2, c3 = st.columns(3)

    #column 1 config
    c1.write('### Date')
    initial_date = c1.date_input('Start date', datetime.date(2021, 11, 1))
    final_date = c1.date_input('End date', datetime.date(2021, 12, 30))

    c1.write('### Hour')
    hr = list(range(24))
    start_hr, end_hr = c1.select_slider('Time', options=hr, value=[0,23])


    #column 2 config
    c2.write('### Group')
    tipo = c2.radio( 'Tipo', ['Todos']+list(set(df['parent label'])))

    #column 3 config
    c3.write('### Vew data as')

    key_list = list(df.keys()) #Lista de columnas
    cath_keys = ['label','date','sensor_name', 'hour','parent label'] #Columnas con variables categoricas
    cont_keys = ['max_f','max_t', 'min_f', 'min_t', 'latitud', 'longitud']#Columnas con variables continuas

    group_options = c3.multiselect(
        'Group by:',
        cath_keys
    )

    
    measure_options = ['Size', 'Mean', 'Max value', 'Min value']

    c3.write('### Visualize')
    vew_options = c3.multiselect(
        'Data to view:',
        cont_keys
    )


    measurements = c3.multiselect(
        'Measurement:',
        measure_options
    )


    st.write('### Plot')
    display_options = ['Bar', 'Line']
    display = st.multiselect('Select plot style', display_options)
    

    if update:

        df_filter = df.copy()

        #Filter parent label
        df_filter = filter_parent_label(df_filter, tipo)

        #Filter date
        df_filter = filter_date(df_filter, initial_date, final_date)

        #Filter hour
        df_filter = filter_hour(df_filter, start_hr, end_hr)

        #Group data
        df_filter = group_data(df_filter, group_options)

        if group_options:

            if 'Line' in display: linep(df_filter)
            if 'Bar' in display: barp(df_filter)
            


        #st.dataframe(df_filter)
        update = False