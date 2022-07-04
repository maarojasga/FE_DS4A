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

from apps.classification import preprocessing_audio, classification

#from st_aggrid.grid_options_builder import GridOptionsBuilder
#from st_aggrid import AgGrid

#import plotly.graph_objects as go
#import plotly.io as pio

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
    uploaded_file = st.file_uploader("Select file",type=["wav"])
    
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
            dfIndex=df_indices_file.reset_index()
            #dfIndex=dfIndex.style.format({"Value":"{:.2f}"})

            ttips=pd.DataFrame(data=[["Acoustic Diversity Index (ADI): Increases with greater evenness across frequency bands.",
                                        "Highest values were from recordings with high levels of geophony or anthrophony (wind, helicopters or trucks)"],
                                        ["Acoustic Complexity Index (ACI): Measure the difference in amplitude between one time sample and the next within a frequency band, relative to the total amplitude within that band.",
                                        "High values indicate storms, intermittent rain drops falling from vegetation, stridulating insects, or high levels of bird activity."],
                                        ["Normalized Difference Soundscape Index (NDSI): Relies on a theoretical frequency split between anthrophony (1–2 kHz) and biophony (2–11 kHz).",
                                        "High values reflect high levels of insect biophony"],
                                        ["Bioacoustic Index (BI): higher values indicate greater disparity between loudest and quietest bands.",
                                        "Highest values produced by blanket cicada noise,Low values arise when there is no sound between 2 and 11 kHz."],
                                        ["Frecuency entropy (Hf): a measure of acoustic energy dispersal through the spectrum","Heavy rain produces a high H[s] value"], #https://stackoverflow.com/questions/30418391/what-is-frequency-domain-entropy-in-fft-result-and-how-to-calculate-it
                                        ["Temporal entropy (Ht): The squared amplitude values of the wave envelope normalized to unit area and treated as a probability mass function (pmf)",np.nan],
                                        ["Acoustic entropy (H): Increases with greater evenness of amplitude among frequency bands and/or time steps.","Highest values come from near‐silent recordings, lowest values produced when insect noise dominated a single frequency band."],
                                        ["Spectral cover (SC)",np.nan],
                                        ["Number of peaks (NP): measure of the average number of peaks in the spectra of the frames through a recording",np.nan],
                                        ],columns=dfIndex.columns, index=dfIndex.index)
            """dfIndexplot= dfIndex.style\
                        .set_tooltips(ttips,props="visibility:hidden; position:absolute; background-color: #DEF3FE;font-size:12px; padding: 10px; border-radius: 7px;z-index:1;")\
                        .set_table_styles([{'selector': 'th','props': [('background-color', '#add8e6')]}])\
                        .hide_index()\
                        .to_html()

            #st.dataframe(dfIndexplot)
            st.markdown(dfIndexplot,unsafe_allow_html=True)
            df_xlsx = to_excel(dfIndex)
            st.download_button(label='📥 Download Indices',
                                data=df_xlsx ,
                                file_name= 'Acoustic Indices.xlsx')"""
            

        st.subheader('Classification of Audio')
        st.markdown('In this section we are going to detect the presence or absence of soundscape components')

        if st.button('Detect Rain'):
            with st.spinner('Executing classifcation...'):

                st.info("Extracting features...")

                features = preprocessing_audio(y, sr)


                st.info("Classifying presence or absence")

                result = classification(features)
                if result ==0:
                    st.success('Result: Audio with rain absence')
                else:
                    st.success('Result: Audio with rain presence')  

                st.success('Classifcation executed successfully')
                st.balloons()

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data

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