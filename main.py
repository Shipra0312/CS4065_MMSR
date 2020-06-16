import pandas as pd
import numpy as np
from pyAudioAnalysis import ShortTermFeatures

import audioBasicIO
from src.extract_series import calculate_energy, calculate_shotboundary, calculate_pitch, calculate_heur, smooth

video_file = "data_extracted/videos/training1.mp4"
audio_file = "data_extracted/videos/audio1.wav"

""""""
"Specify parameters"
""""""
output_dir = ""  # directory of the output file
chuncksize = 1  # arousal per how many seconds
heur = False  # whenether we include the event data of the game

""""""
"Obtain  sequences"
""""""
serie_energy = calculate_energy(audio_file, chuncksize=chuncksize)
serie_pitch = calculate_pitch(audio_file, chuncksize=chuncksize)
serie_shotboundary = calculate_shotboundary(video_file, chuncksize=chuncksize)

""""""
"Smooth serie using kaiser filter"
""""""
serie_energy_smoothed = smooth(serie_energy, 0.1)
serie_shotboundary_smoothed = smooth(serie_shotboundary, 0.1)
serie_pitch_smoothed = smooth(serie_shotboundary, 0.1)


# [Fs, x] = audioBasicIO.read_audio_file(audio_file)
# x = audioBasicIO.stereo_to_mono(x)
# overlap = 0.5*Fs
# F, f_names = ShortTermFeatures.feature_extraction(x, Fs, Fs, overlap) #takes approx. 2.5 mins to complete


"""
"Normalize series and combine them"
"""
