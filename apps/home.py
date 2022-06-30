import streamlit as st
from PIL import Image
from pydub import AudioSegment
import numpy as np
import librosa
from matplotlib import pyplot as plt
import librosa.display
from io import BytesIO
import matplotlib as mpl
import plotly.express as px



def app():
    plt.style.use('default')

    st.write(
        """
        # Acoustic biodiversity monitoring
        #
        """
    )
    image = Image.open('images/amazonia-1.jpg')
    st.image(image, caption='Amazonas')


    st.write("## Upload your track to analyze")
    uploaded_file = st.file_uploader("Select file",type="wav")
    if uploaded_file is not None:
        named_colorscales = plt.colormaps()
        default_ix = default_ix = named_colorscales.index('viridis')
        colours = st.sidebar.selectbox(('Choose a colour pallete'), named_colorscales, index=default_ix)

        audio_bytes = uploaded_file.read()
        st.audio(audio_bytes, format='audio/mp3')
        st.write("Spectogram:")
        # Side Bar #######################################################
        y, sr = handle_uploaded_audio_file(uploaded_file)
        col1, col2 = st.columns([1,1])
        with col1:
            st.markdown(
            f"<h4 style='text-align: left; color: black;'>Original</h5>",
            unsafe_allow_html=True,
        )
            buf = BytesIO()
            plot_transformation(y, sr, "Original",colours).savefig(buf, format="png")
            st.image(buf)

            #st.pyplot(plot_transformation(y, sr, "Original"))

        with col2:
            st.markdown(
            f"<h4 style='text-align: left; color: black;'>Wave plot </h5>",
            unsafe_allow_html=True,
        )
            buf = BytesIO()
            plot_wave(y, sr).savefig(buf, format="png")
            st.image(buf)
            #st.pyplot(plot_wave(y, sr))

        #nyquist_frequency = int(audio_bytes.sampling_frequency/2)
        #maximum_frequency = st.sidebar.slider('Maximum frequency (Hz)', 5000, nyquist_frequency, 5500)
    

    #image = Image.open('images/amazonia-1.jpg')

    #st.image(image, caption='Amazonas')

def handle_uploaded_audio_file(uploaded_file):
    a = AudioSegment.from_file(
        file=uploaded_file, format=uploaded_file.name.split(".")[-1]
    )

    channel_sounds = a.split_to_mono()
    samples = [s.get_array_of_samples() for s in channel_sounds]

    fp_arr = np.array(samples).T.astype(np.float32)
    fp_arr /= np.iinfo(samples[0].typecode).max

    return fp_arr[:, 0], a.frame_rate

def plot_transformation(y, sr, transformation_name,colours):
    D = librosa.stft(y)  # STFT of y
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    fig, ax = plt.subplots(figsize=(7,4))
    img = librosa.display.specshow(S_db, x_axis="time", y_axis="linear", ax=ax,cmap=colours)
    fig.colorbar(img, ax=ax, format="%+2.f dB")

    return plt.gcf()

def plot_wave(y, sr):
    fig, ax = plt.subplots(figsize=(7,4))
    img = librosa.display.waveshow(y, sr=sr, x_axis="time", ax=ax)
    return plt.gcf()

