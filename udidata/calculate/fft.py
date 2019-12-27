import numpy as np
import pandas as pd


#######################################################################################################################

def fft(signal, sampling_rate):
    
    """
    Parameters
    ----------
    signal: array-like
        An array with discrete signal values
    
    sampling_rate: int
        Number of samples per one cycle of a unit time.

    Returns
    -------
    S, freq: tuple
        Tuple of two arrays one for intensity (PSD), one for frequency domain
    """
    Ts = 1/sampling_rate    # sampling spacing - inverse of sampling rate
    N = len(signal)    # number of sampled points
    
    S = np.fft.rfft(signal)
    S = np.abs(S)/N    # normalize frequency
    freq = np.fft.rfftfreq(N, Ts)    # frequecny domain

    return pd.Series(S, index=pd.Index(freq, name="freq"))
    
    