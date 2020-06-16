import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import moviepy.editor as mp


import audioBasicIO
from src.extract_highlights import extract_highlight_df
from src.extract_series import calculate_energy, calculate_shotboundary, calculate_pitch, smooth, \
    extract_extract_audioAnalysis
from src.process_features import process_features

""""""
"Specify parameters"
""""""
output_dir = ""  # directory of the output file
chuncksize = 1  # arousal per how many seconds

video_file = "data_extracted/videos/training1.mp4"
audio_file = "data_extracted/videos/audio1.wav"

clip = mp.VideoFileClip(video_file)
clip.audio.write_audiofile(audio_file)

""""""
"Obtain  sequences"
""""""
print(" Start Obtain Sequences")
serie_energy = calculate_energy(audio_file, chuncksize=chuncksize)
# serie_pitch = calculate_pitch(audio_file, chuncksize=chuncksize)
serie_shotboundary = calculate_shotboundary(video_file, chuncksize=chuncksize)
zcr, spec_cent, spec_spread, sprec_entr, spec_flux, spec_rolloff = extract_extract_audioAnalysis(audio_file,
                                                                                                 chuncksize=1)

print(" Finish Obtain Sequences")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Process the features"
"1.Fix Serie to 0.99 quantile to avoid extreme values"
"2.Smooth serie using kaiser filter"
"3. Normalize the features"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
print("Start processing sequences")

# inverse shot changes
serie_shotboundary = 1 / (serie_shotboundary + 0.1)
seconds = len(serie_shotboundary)

# series = [serie_energy, serie_pitch, serie_shotboundary, zcr, spec_cent]
series = [serie_energy, serie_shotboundary, zcr, spec_cent, spec_flux]
processed = process_features(series, seconds, quant=0.99, window_length=150, smooth_beta=0.1)

print("Finish processing sequences")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Normalize series and combine them"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

print("Combining curves and extracting highlights")
weights = [10, 10, 0.01, 0.1, 1]
curve = np.zeros(processed[0].shape)
for i in range(len(weights)):
    curve = np.add(curve, weights[i] * processed[i])

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"Extract highlight videos"
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
highlight_df = extract_highlight_df(curve, threshold=0.375, min_sec_highlight=10)