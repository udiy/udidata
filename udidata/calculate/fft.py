import numpy as np
import pandas as pd


#######################################################################################################################

def rfft(signal, sampling_rate):
    
    """
    Computes the power spectrum of a time series (signal) with real values.

    Parameters
    ----------
    signal: array-like
        An array with real signal values.
    
    sampling_rate: int
        Sampling rate or sampling frequency. Number of samples per a unit time.
        
    Returns
    -------
    : pandas Series
        A pandas series with complex numbers representing frequecny spectrum. 
        Index is freqeuncy, in units of cycles per unit time
    """
    
    spectra = np.fft.rfft(signal)
    freq = np.fft.rfftfreq(n=signal.size, d=(1/sampling_rate))
    
    return pd.Series(spectra, index=pd.Index(freq, name="freq"))

#######################################################################################################################