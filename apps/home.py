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
from maad import sound, features, util
import pandas as pd

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
        file_var = AudioSegment.from_wav(uploaded_file)

        target_fs = 48000
        file_var.export("1.wav", format="wav")
        s, fs = sound.load("1.wav")
        s = sound.resample(s, fs, target_fs, res_type='kaiser_fast')
        Sxx, tn, fn, ext = sound.spectrogram(
            s, target_fs, nperseg = 1024, noverlap=0, mode='amplitude')
        df_indices_file = compute_acoustic_indices(s, Sxx, tn, fn)

        st.audio(audio_bytes, format='audio/mp3')
        st.write("Spectogram:")
        # Side Bar #######################################################
        y, sr = handle_uploaded_audio_file(uploaded_file)
        col1, col2, col3 = st.columns([1,1,1])
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

        with col3:
            st.markdown(
            f"<h4 style='text-align: left; color: black;'>Acoustic Indices</h5>",
            unsafe_allow_html=True,
        )
            st.table(df_indices_file)
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

def compute_acoustic_indices(s, Sxx, tn, fn):
    """
    Parameters
    ----------
    s : 1d numpy array
        acoustic data
    Sxx : 2d numpy array of floats
        Amplitude spectrogram computed with maad.sound.spectrogram mode='amplitude'
    tn : 1d ndarray of floats
        time vector with temporal indices of spectrogram.
    fn : 1d ndarray of floats
        frequency vector with temporal indices of spectrogram..
    Returns
    -------
    df_indices : pd.DataFrame
        Acoustic indices
    """
    
    # Set spectro as power (PSD) and dB scales.
    Sxx_power = Sxx**2
    Sxx_dB = util.amplitude2dB(Sxx)

    # Compute acoustic indices
    ADI = features.acoustic_diversity_index(
        Sxx, fn, fmin=2000, fmax=24000, bin_step=1000, index='shannon', dB_threshold=-70)
    _, _, ACI = features.acoustic_complexity_index(Sxx)
    NDSI, xBA, xA, xB = features.soundscape_index(
        Sxx_power, fn, flim_bioPh=(2000, 20000), flim_antroPh=(0, 2000))
    Ht = features.temporal_entropy(s)
    Hf, _ = features.frequency_entropy(Sxx_power)
    H = Hf * Ht
    BI = features.bioacoustics_index(Sxx, fn, flim=(2000, 11000))
    NP = features.number_of_peaks(Sxx_power, fn, mode='linear', min_peak_val=0, 
                                  min_freq_dist=100, slopes=None, prominence=1e-6)
    SC, _, _ = features.spectral_cover(Sxx_dB, fn, dB_threshold=-50, flim_LF=(1000,20000))
    
    # Structure data into a pandas series
    df_indices = pd.DataFrame.from_dict({
        'ADI': [ADI],
        'ACI':[ACI],
        'NDSI': [NDSI],
        'BI': [BI],
        'Hf': [Hf],
        'Ht': [Ht],
        'H': [H],
        'SC': [SC],
        'NP': [int(NP)]},orient="index",columns=["Value"])
    
    return df_indices