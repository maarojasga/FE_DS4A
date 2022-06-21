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

    @st.cache
    @st.cache(allow_output_mutation=True)#temporal
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
        

    #    return df


    def update():
        update = True


    
    df = read_data()
    df['date'] = df['Fecha'].dt.date #adding date column (temporal)

    #set columns
    c1, c2, c3 = st.columns(3)

    #column 1 config
    c1.write('### Rango de fechas')
    initial_date = c1.date_input('Fecha de inicio', datetime.date(2021, 11, 1))
    final_date = c1.date_input('Fecha final', datetime.date(2021, 12, 30))

    c1.write('### Rango de hora')
    hr = list(range(24))
    start_hr, end_hr = c1.select_slider('Hora', options=hr, value=[0,23])


    #column 2 config
    c2.write('### Grupo')
    tipo = c2.radio( 'Tipo', ['Todos']+list(set(df['parent label'])))

    #column 3 config
    c3.write('### Ver datos como')

    key_list = list(df.keys()) #Lista de columnas
    cath_keys = ['label','date','sensor_name', 'hour','parent label'] #Columnas con variables categoricas
    cont_keys = ['max_f','max_t', 'min_f', 'min_t', 'latitud', 'longitud']#Columnas con variables continuas

    group_options = c3.multiselect(
        'Agrupar elementos por:',
        cath_keys
    )

    

    #c3.write('### Calcular')


    c3.write('### Tipo gráfico')
    #display_options = c3.multiselect()

    
    #Button to print
    #filtrar = st.button('Filtrar')
    

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

        #st.write(group_options)

        st.dataframe(df_filter)
        update = False