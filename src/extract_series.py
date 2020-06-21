import aubio
import librosa
import numpy as np
import cv2
from pyAudioAnalysis import ShortTermFeatures

import audioBasicIO


def calculate_energy(audiofile, chuncksize=1, sample_rate=44100):
    audio_file = audiofile
    z, sample_rate = librosa.load(audio_file, sr=sample_rate)
    int(librosa.get_duration(z, sample_rate) / 60)

    window_length = chuncksize * sample_rate
    amplitude = z[21 * window_length: 22 * window_length]
    # ipd.Audio(amplitude, rate=sample_rate)

    # Calculate the energy for each chunk
    energy = np.array([sum(abs(z[i:i + window_length] ** 2)) for i in range(0, len(z), window_length)])
    return energy[1:]


def calculate_pitch(audiofile, chuncksize=1, sample_rate=11025):
    Fs = sample_rate

    win_s = chuncksize * Fs  # fft size
    hop_s = chuncksize * Fs  # hop size

    s = aubio.source(audiofile, sample_rate, hop_s)
    samplerate = s.samplerate

    pitch_o = aubio.pitch("yin", win_s, hop_s, samplerate)
    pitches = []
    total_frames = 0

    while True:
        samples, read = s()
        pitch = pitch_o(samples)[0]
        if pitch < 0:
            pitch = 0
        pitches += [pitch]
        total_frames += read
        if read < hop_s:
            break
    return pitches[1:]


def calculate_shotboundary(video_file, chuncksize=1):
    vidcap = cv2.VideoCapture(video_file)

    fps = vidcap.get(cv2.CAP_PROP_FPS)
    frameCount = int(vidcap.get(cv2.CAP_PROP_FRAME_COUNT))
    frameWidth = int(vidcap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frameHeight = int(vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    previous_histogram = None

    count = 1
    success = True
    frame_index = 0
    scores = []

    while success:
        success, image = vidcap.read()
        if frame_index % np.rint(chuncksize * count * fps) != 0:
            frame_index += 1
            continue
        elif frame_index > frameCount:
            break
        else:
            frame_index += 1
            count += 1

            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            histogram = cv2.calcHist([image], [0], None, [256], [0, 256])

            if previous_histogram is None:
                previous_histogram = histogram
                count += 1
                continue

            score = cv2.compareHist(previous_histogram, histogram, cv2.HISTCMP_CHISQR)

            scores.append(score)

            previous_histogram = histogram

            if cv2.waitKey(10) == 27:  # exit if Escape is hit
                break
    return np.array(scores)


def extract_extract_audioAnalysis(audio_file, chuncksize=1):
    [Fs, x] = audioBasicIO.read_audio_file(audio_file)
    x = audioBasicIO.stereo_to_mono(x)
    overlap = chuncksize * Fs
    F, f_names = ShortTermFeatures.feature_extraction(x, Fs, Fs, overlap)  # takes approx. 2.5 mins to comple

    # return Zero Crossing Rate, Spectral Centroid, Spectral Spread, Spectral Entropy, Spectral Flux, Spectral Rolloff
    return F[0], F[3], F[4], F[5], F[6], F[7]

