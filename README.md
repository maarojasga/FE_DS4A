# FE_DS4A
Repository created for the DS4A project


# Steps to run app in gcloud

1. Update from git to server:
cd FE_DS4A ; git fetch ; git pull

2. Run venv:
source venv/bin/activate

3. Run app:
streamlit run app.py --server.port 8080

4. Load page:
http://34.71.183.243:8080


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

 #About Tadular Data
 
 The web-tool presents data recolected and provided by Humboldt institute. Main fields are:
 
 1. sensor_name: A code that identifies each sensor use to recolect data.
 2. fname: Name of .wav file
 3. date: the date in which the recordings were made. 
 4. time: the hour of recording.
 5. decimalLon and decimalLat: Latitude and longitude of sensor.
 6. label: describes if record has sounds of 
 
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
 
