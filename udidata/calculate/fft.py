import numpy as np
import pandas as pd


#######################################################################################################################

def fft(signal, sampling_rate, positive=False, spectrum=None):
    
    """
    Parameters
    ----------
    signal: array-like
        An array with discrete signal values.
    
    sampling_rate: int
        Number of samples per one cycle of a unit time.

    positive: bool
        If true, return only positive frequency values

    spectrum: str
        Type of spectral values to return. Options: "amp" - amplitude, "psd" - power spectral density (amplitude sqaured).
        If None than complex numbers will be returned

    Returns
    -------
    S: pandas.Series
        A pandas series whose values is the frequecny spectrum, and index is freqeuncy values
    """

    # compute frequency spectrum using fft
    S = np.fft.fft(signal)
    
    # compute frequency range (frequency axis values)
    n = signal.size
    d = (1/sampling_rate)   # sampling spacing - inverse of sampling rate
    freq = np.fft.fftfreq(n, d)

    # cast S into a pandas Series with frequency values as index
    S = pd.Series(S, index=pd.Index(freq, name="freq"))

    if spectrum == "amp":
        S = S.abs()
    elif spectrum == "psd":
        S = (S.abs() ** 2)
    
    if positive:
        # slice S to select only positive frequency values
        return S.iloc[:int(n/2)]

    return S