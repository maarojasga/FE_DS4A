
# Listening the Magdalena Medio Wildlife for biodiversity conservation using data science and acoustic sensors

The human ecological footprint has had a tremendous effect on the environment and biodiversity. Therefore to develop cost-effective solutions for monitoring ecological diversity is a must. In this project, we generate solutions to the problem of acoustic characterization of the ecosystem in Magdalena Medio using sensors in passive acoustic monitoring (PAM). We detect an classify sounds present in .wav recordings into 4 categories: rain, birds, insects, and humans, right away the results are presented through a streamlit web app.

As stated in advance, the web application was deployed using Streamlit. The classification algorithms use scikit-maad. Another relevant libraries are pandas and librosa. A full list with required libraries is presented in the requirements.txt file present in this repo.

# Install and run

## Cloning this repo

1. Copy the url prensented in this repo (Highlighted in blue):

 ![image](https://user-images.githubusercontent.com/99512774/177884173-8ef1becf-e662-4794-9028-c64fc2bb59b4.png)
 
2. Open a terminal
3. Go to preferred directory path
4. Run: git clone <project-url> where <project-url> is the url you copy on step 1.


## Creating a virtual environment and install requirements

To ensure correct operation, we recommend creating a virtual environment and installing the necessary libraries present in the requirements.txt file. We present two ways to do it

### Using menv:

1. Open a terminal 
2. Go to preferred directory path 
3. On terminal: python -m venv project_name  *example* python -m venv listening_magd
4. Run: project_name\Scripts\activate.bat
5. Install requirements: pip install -r requirements

### Using conda:

1. Open a terminal 
2. Go to preferred directory path 
3. On terminal: conda create -n project_name  *example* conda create -n listening_magd
4. Run: conda activate project_name
5. Install requirements: pip install -r requirements

Run application by using: streamlit run app.py.

# Data

## Tabular data
 The web-tool presents data recolected and provided by Humboldt institute. Main fields are:
 
 1. **sensor_name:** A code that identifies each sensor use to recolect data.
 2. **fname:** Name of .wav file
 3. **date:** the date in which the recordings were made. 
 4. **time:** the hour of recording.
 5. **decimalLon and decimalLat:** Latitude and longitude of sensor.
 6. **label:** describes if record has sounds of Bat, Insect, Rain, Pulse, Herpetus, anthrophony, Birds, Motor, Indeterminate, Steps, Water Flow, domesticated animals or if sound is saturated.
 7. **grand_label:** Classifies type of sounds into 4 categories: Other, biophony, geophony, anthrophony
 8. **ecosystem:** Describes type of ecosystem in which recordings were made: palm, grassland, riparian forest, grasses, dense forest, open forest
 9. **Acoustic indices:** Nine indices that help us to characterize the properties of the signal, they are used to describe some aspect of the spectral and temporal diversity or complexity of sounds presented in .wav files: <br /> 
    **a) ADI:** (Acoustic Diversity Index) Increases with greater evenness across frequency bands. Highest values were from recordings with high levels of geophony or anthrophony (wind, helicopters or trucks)<br />
    **b) ACI:** (Acoustic Complexity Index) Measure the difference in amplitude between one time sample and the next within a frequency band, relative to the total amplitude within that band. High values indicate storms, intermittent rain drops falling from vegetation, stridulating insects, or high levels of bird activity. <br />
    **c) NDSI:** (Normalized Difference Soundscape Index): Relies on a theoretical frequency split between anthrophony (1–2 kHz) and biophony (2–11 kHz). High values reflect high levels of insect biophony <br />
    **d) BI:** (Bioacoustic Index) higher values indicate greater disparity between loudest and quietest bands. Highest values produced by blanket cicada noise, Low values arise when there is no sound between 2 and 11 kHz. <br />
    **e) Hf:** (Frecuency entropy) a measure of acoustic energy dispersal through the spectrum, heavy rain produces a high values. <br />
    **f) Ht:** (Temporal entropy) The squared amplitude values of the wave envelope normalized to unit area and treated as a probability mass function (pmf) <br />
    **g) H:** (Acoustic entropy) Increases with greater evenness of amplitude among frequency bands and/or time steps. Highest values come from near‐silent recordings, lowest values produced when insect noise dominated a single frequency band. <br />
    **h) SC:** (Spectral cover) <br />
    **i) NP:** (Number of peaks) measure of the average number of peaks in the spectra of the frames through a recording.     <br />

## Recordings
 All recordings analized are available in: https://www.dropbox.com/sh/9hm5grr21jjppm2/AAAjQLdqOUxqVCx00Ir2-ZXxa?dl=0
 Some recordings to test this application are available in audio_test folder in this repo.
 
# Web-app
 Web application has 4 principal sections:
 
 ## Home:
 Here you can see do a minimal test of of the proposed algorithms:
 
 <p align="center">
 <img src="https://user-images.githubusercontent.com/99512774/177885346-4ded7892-ee84-45aa-a982-bd020c21a692.png" width=50% height=50%>
  </p>
 You can upload a .wav file and see the spectrogram and calculated acoustic indices of uploaded record.
 
 <p align="center">
 <img src="https://user-images.githubusercontent.com/99512774/177886705-b4631102-1199-42f4-a624-6b5ccb65c176.png" width=50% height=50%>
 </p>
 Finally, by using *Detect* button the algorithm identifies if there is rain presence or absence:
 
 <p align="center">
<img src="https://user-images.githubusercontent.com/99512774/177887034-03082c13-e82f-4eb9-a548-db6602f25998.png" width=50% height=50%>
 </p>

 ## Maps:
 
 Here you can see a map indicating the site where recording were made. You can filter by Category of classified recordings:

<p align="center">
<img src="https://user-images.githubusercontent.com/99512774/177888392-3e38ea52-30c9-4ff0-bb89-8fb38f3dd111.png" width=50% height=50%>
 </p>
 
 ## Table:
 
 A 2d table visual of data recolected by recording, such as latitude and longitude, sensor type, date and grand label (Biophony, anthrophony, geophony etc) You can select a column to see data grouped using the controls.
 <p align="center">
<img src="https://user-images.githubusercontent.com/99512774/177889282-17bab976-5463-476b-9d14-b331e5a0dc86.png" width=50% height=50%>
 </p>
 
 ## Layout:
 A tool to visualize data presented filtered by date and Category. the graphs present are according to the type of data that is being ploted
 
 <p align="center">
<img src="https://user-images.githubusercontent.com/99512774/177889559-51006598-4ed5-4203-b588-3801c02fefab.png" width=50% height=50%>
 </p>
 
 <p align="center">
<img src="https://user-images.githubusercontent.com/99512774/177890157-cabe3853-c1d0-4d55-8d8f-d26abb9488a4.png" width=50% height=50%>
 </p>
 
