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
        df = pd.read_csv('data/Labeled Metatabla.csv')
        df['date'] = pd.to_datetime(df['date'])
        return df

    def filter_parent_label(df, tipo):
        update()
        if tipo == 'All': return df
        else:
            df_filter = df[df['grand_label'] == tipo]
            return df_filter

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

    def group_data(df, group_option, agg = 'size'):
        if group_option:
            df_gb = df.groupby(group_option)
            df_g = df_gb.aggregate(agg)
            df_g = pd.DataFrame(df_g)
            return df_g
        
        else: return df

    def update():
        update = True

    df = read_data()

    #set columns
    c1, c2, c3 = st.columns(3)

    #column 1 config
    c1.write('### Date select')
    initial_date = c1.date_input('Start date', datetime.date(2021, 11, 1))
    final_date = c1.date_input('End date', datetime.date(2021, 12, 30))

    c1.write('### Time select')
    hr = list(range(24))
    start_hr, end_hr = c1.select_slider('Time', options=hr, value=[0,23])


    #column 2 config
    c2.write('### Biophonic group')
    tipo = c2.radio( 'Type', ['All']+list(set(df['grand_label'])))

    #column 3 config
    c3.write('### Vew as')

    key_list = [
        'eventID',
        'sensor_name',
        'date2',
        'hour',
        'decimalLat',
        'decimalLon',
        'grand_label',
        'label_desc',
        'Cobertura',
        'GrupoBiolo',
        'Presión sonora 1',
        'Presión sonora 2',
        'Presión sonora 3',
        'Presión sonora 4',
        'min_f',
        'max_f',
        'min_t',
        'max_t',
        'BI',
        'NP',
        'ACI',
        'NDSI',
        'ADI',
        'H',
        'Ht',
        'Hf',
        'SC'
    ]

    cath_keys = [
        'eventID',
        'sensor_name',
        'date2',
        'hour',
        'grand_label',
        'label_desc',
        'Cobertura',
        'GrupoBiolo',
        ] #Categorical variables columns

    aggregate_fns = [
        'count',
        'size',
        'sum',
        'mean',
        'median',
        'std',
        'describe',
        'min',
        'max'
    ]

    cont_keys = [key for key in key_list if key not in cath_keys]#Cont variables columns

    group_options = c3.multiselect(
        'Group by:',
        cath_keys
    )


    to_display = c3.selectbox(
        'Parameters to check:',
        aggregate_fns
    ) 

    if update:

        df_filter = df.copy()

        #Filter grand_label
        df_filter = filter_parent_label(df_filter, tipo)

        #Filter date
        df_filter = filter_date(df_filter, initial_date, final_date)

        #Filter hour
        df_filter = filter_hour(df_filter, start_hr, end_hr)

        #Group data
        df_filter = group_data(df_filter, group_options, to_display)


        st.dataframe(df_filter)
        update = False

    with c3:
        st.download_button("Download table",data=pd.DataFrame.to_csv(df_filter,index=False))