from sklearn.preprocessing import normalize

from src.extract_series import smooth
import numpy as np


def process_features(series, seconds, quant=0.99, window_length=150, smooth_beta=0.1):
    processed = []

    for serie in series:
        serie = serie.ravel()
        serie[serie > np.quantile(serie, quant)] = np.quantile(serie, quant)
        serie = smooth(serie, smooth_beta, window_len=window_length)
        serie = normalize(serie.reshape(1, -1)).ravel()
        processed.append(serie[0:seconds])
    return processed
