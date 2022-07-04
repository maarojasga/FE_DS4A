import streamlit as st
from PIL import Image
class MultiApp:

    def __init__(self):
        self.apps=[]

    def add_app(self, title, func):

        self.apps.append(
            {
                "Titulo":title,
                "Funcion": func
            }
        )

    def run(self):
        local_css("styles.css")
        #st.set_page_config(page_title='DS4A', layout="wide",page_icon=Image.open('images/ave.png'))
        #st.markdown(f'<div class="appview-container css-1wrcr25 egzxvld4" data-testid="stAppViewContainer" data-layout="narrow">',unsafe_allow_html=True)
        st.sidebar.title('Acoustic biodiversity monitoring')
        app= st.sidebar.radio(
            '',
            self.apps,
            format_func = lambda app: app['Titulo']
        )

        

        app['Funcion']()

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

