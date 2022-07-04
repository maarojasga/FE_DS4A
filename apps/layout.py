from cProfile import label
from cmath import nan
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import datetime
import plotly.express as px
import numpy as np


def app():


    plt.style.use('ggplot')
    plt.style.use('dark_background')

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


#Plot options

    #bar plot
    def bar_plot(df, var):
        update()
        st.write('# ')
        st.write('# ')
        st.write('# ')
        st.subheader('Bar plot of ' + var + ' data')
        st.bar_chart(df.groupby(var).size())
    
    #histogram
    def histogram_plot(df,var,bns):
        update()
        st.subheader('Histogram of ' + var + ' data')
        hist_values = np.histogram(df[var], bins=bns,)[0]
        st.bar_chart(hist_values)

    #Scatter plot
    def scatter_plot(df,var_x,var_y):
        update()
        st.subheader('Scatter plot of %s VS %s' % (var_x, var_y))
        fig = px.scatter(
            x = df[var_x],
            y = df[var_y],
        )
        fig.update_layout(
            xaxis_title = var_x,
            yaxis_title = var_y,
            width=600, height=600,
        )

        st.write(fig)

    #Cont Heatmap
    def cont_heatmap(df,var_x,var_y):
        update()
        st.subheader('Heatmap of %s VS %s' % (var_x, var_y))

        fig = px.density_heatmap(
            x = df[var_x],
            y = df[var_y],
            width=600, height=600,
        )
        fig.update_layout(
            xaxis_title = var_x,
            yaxis_title = var_y,
        )

        st.write(fig)


    #Box plot
    def box_plot(df,var_x,var_y):
        update()
        st.subheader('Box plot of %s VS %s' % (var_x, var_y))
        fig = px.box(
            x = df[var_x],
            y = df[var_y],
            width=600, height=600,
        )
        fig.update_layout(
            xaxis_title = var_x,
            yaxis_title = var_y,
        )

        st.write(fig)

    #Strip plot

    def strip_plot(df,var_x,var_y):
        update()
        st.subheader('Strip plot of %s VS %s' % (var_x, var_y))
        fig = px.strip(
            x = df[var_x],
            y = df[var_y],
            width=600, height=600,
        )
        fig.update_layout(
            xaxis_title = var_x,
            yaxis_title = var_y,
        )

        st.write(fig)

    #Sunburst
    def sunburst_plot(df,var_x,var_y):
        update()
        st.subheader('Sunburst plot of %s containing %s' % (var_x, var_y))
        fig = px.sunburst(
            df, path=[var_x,var_y],
            width=600, height=600,
        )
        
        st.write(fig)

    df = read_data()

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

    cont_keys = [key for key in key_list if key not in cath_keys]#Cont variables columns


    #set columns
    c1, c2, c3 = st.columns([1, 2, 2])

    #column 1 config
    c1.write('### Set Variables')
    x_option = c1.selectbox(
        'Horizontal axis:',
        ['None'] + key_list
    )
    y_option = c1.selectbox(
        'Vertical axis:',
        ['None'] + key_list
    )


    c1.write('### Date select')
    initial_date = c1.date_input('Start date', datetime.date(2021, 11, 1))
    final_date = c1.date_input('End date', datetime.date(2021, 12, 30))

    c1.write('### Time select')
    hr = list(range(24))
    start_hr, end_hr = c1.select_slider('Time', options=hr, value=[0,23])
    c1.write('### Category')
    tipo = c1.radio( 'Label', ['All']+list(set(df['grand_label'])))

    display_options = ['Bar plot', 'Histogram', 'Box plot', 'Scatter plot']

    

    if update:

        df_filter = df.copy()

        #Filter parent label
        df_filter = filter_parent_label(df_filter, tipo)

        #Filter date
        df_filter = filter_date(df_filter, initial_date, final_date)

        #Filter hour
        df_filter = filter_hour(df_filter, start_hr, end_hr)

            #Show hist and bar plots
        if x_option != 'None':
            if x_option in cath_keys:
                x_active = True
                x_cath = True
               
            elif x_option in cont_keys:
                x_active = True
                x_cath = False
               
            else:
                x_cath == nan
            
        else: x_active = False


        if y_option != 'None':
            if y_option in cath_keys:
                y_active = True
                y_cath = True

            elif y_option in cont_keys:
                y_active = True
                y_cath = False

            else:
                y_cath == nan
        else: y_active = False

        with c2:
            if x_active == True:
                if x_cath:
                    bar_plot(df_filter, x_option)

                if x_cath==False:
                    bnsx = st.slider('Select number of bins', 1, 50, 10,key=0)
                    histogram_plot(df_filter,x_option,bnsx)
            
            #activate c1 plot 
            if x_active and y_active:

                if x_cath and y_cath:
                    sunburst_plot(df_filter, x_option, y_option)

                if not x_cath and not y_cath:
                    scatter_plot(df_filter, x_option, y_option)

                if (x_cath and not y_cath) or (y_cath and not x_cath):
                    strip_plot(df_filter, x_option, y_option)         


        with c3:
            if y_active == True:
                if y_cath:
                    bar_plot(df_filter, y_option)

                if y_cath == False:
                    bnsy = st.slider('Select number of bins', 1, 50, 10, key=1)
                    histogram_plot(df_filter,y_option,bnsy)

            #activate c2 plot 
            if x_active and y_active:

                if x_cath and y_cath:
                    cont_heatmap(df_filter, x_option, y_option)

                if not x_cath and not y_cath:
                    cont_heatmap(df_filter, x_option, y_option)
                
                if (x_cath and not y_cath) or (y_cath and not x_cath):
                    box_plot(df_filter, x_option, y_option)
                
        update = False