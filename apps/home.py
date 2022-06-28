import streamlit as st
from PIL import Image
from pydub import AudioSegment

def app():
    st.write(
        """
        # Acoustic biodiversity monitoring
        #
        """
    )
    st.write("## Upload your track to analyze")
    uploaded_file = st.file_uploader("Seleccione archivo")
    if uploaded_file is not None:
        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/mp3')
    

    #image = Image.open('images/amazonia-1.jpg')

    #st.image(image, caption='Amazonas')