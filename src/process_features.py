from sklearn.preprocessing import normalize
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


def smooth(x, beta, window_len=100):
    """ Kaiser smoothing """
    s = np.r_[x[window_len - 1:0:-1], x, x[-1:-window_len:-1]]
    w = np.kaiser(window_len, beta)
    y = np.convolve(w / w.sum(), s, mode='valid')
    return y[int(window_len / 2 - 1):-int(window_len / 2)]
