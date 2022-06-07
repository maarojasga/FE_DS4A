import streamlit as st
from PIL import Image

def app():
    st.write(
        """
        # Acoustic biodiversity monitoring
        #

        """
    )

    image = Image.open('images/amazonia-1.jpg')

    st.image(image, caption='Amazonas')