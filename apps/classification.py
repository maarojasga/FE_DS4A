import pandas as pd
import numpy as np
import librosa as lr

from librosa import feature
from maad import sound, features
from maad.util import power2dB
from joblib import load


target_fs = 10000


def transform(s, fs, wtype='hann', nperseg=512, noverlap=0, db_range=60, db_gain=30):
    """ Compute decibel spectrogram """
    Sxx, tn, fn, ext = sound.spectrogram(s, fs, wtype, nperseg, noverlap)            
    #Sxx = util.power2dB(Sxx, db_range, db_gain)
    Sxx = power2dB(Sxx, db_range, db_gain)
    return Sxx, tn, fn, ext

def preprocessing_audio(y, sr):

    """
    Reading and extracting features
    """

    s, fs = y, sr
    # resample
    s_resamp = sound.resample(s, fs, target_fs, res_type='kaiser_fast')

    # Mel-frequency cepstral coefficients (MFCCs)
    mfcc = feature.mfcc(y=s_resamp, sr=target_fs, n_mfcc=20, n_fft=1024, 
                        win_length=1024, hop_length=512, htk=True)
    mfcc = np.median(mfcc, axis=1)
    # format dataframe
    idx_names = ['mfcc_' + str(idx).zfill(2) for idx in range(1,mfcc.size+1)]
    row = pd.Series(mfcc, index=idx_names)
    
    # Format the output as an array for decomposition
    Sxx, tn, fn, ext = transform(s, fs, nperseg=1024, noverlap=512) #db_range, db_gain)
    # compute shape features
    shape, params = features.shape_features(Sxx)
    all_features = row.append(shape.squeeze(axis=0))

    return pd.DataFrame(all_features).T

def classification(instace):

    model_file_rain = "apps/models/Rain_gbrt_20220703.pkl"
    classifier_rain = load(model_file_rain)
    result_rain = classifier_rain.predict(instace)

    model_file_insects = "apps/models/Insects_gbrt_20220703.pkl"
    classifier_insects = load(model_file_insects)
    result_insects = classifier_insects.predict(instace)

    model_file_birds = "apps/models/Birds_gbrt_20220703.pkl"
    classifier_birds = load(model_file_birds)
    result_birds = classifier_birds.predict(instace)

    model_file_anthro = "apps/models/Anthrophony_gbrt_20220703.pkl"
    classifier_anthro = load(model_file_anthro)
    result_anthro = classifier_anthro.predict(instace)

    if result_rain == 1:
        return 'Geophony: Rain 🌧️ 🌧️ 🌧️ 🌧️'
    elif result_insects == 1:
        return 'Biophony: Insects 🦗 🐜 🦗 🐛'
    elif result_birds == 1:
        return 'Biophony: Birds 🦜 🐦 🦜 🐦 '
    elif result_anthro == 1:
        return 'Anthropophony: 🛵  🛩️  🛵  🛩️'
    else:
        return 'Sound not detected ❌ 😖 ❌ 😖'

