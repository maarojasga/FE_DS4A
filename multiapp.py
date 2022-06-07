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
        st.set_page_config(page_title='DS4A', layout="wide",page_icon=Image.open('images/ave.png'))
        st.sidebar.title('Acoustic biodiversity monitoring')
        app= st.sidebar.selectbox(
            '',
            self.apps,
            format_func = lambda app: app['Titulo']
        )

        

        app['Funcion']()

