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

