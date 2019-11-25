import numpy as np


#######################################################################################################################

def fft(signal, sampling_rate):
    """
    Computes fft for given signal, normalizing results and returns spectrum, and frequency arrays
    
    Parameters
    ----------
    signal : array-like
        An array with discrete signal values
    
    sampling rate : int
        Number of data points per unit time. e.g. 365 for a year, means 1 data point for a day.
    
    Returns
    -------
     : tuple
        Tuple of arrays for spectrum data and frequency data
    """
    n = signal.size
    Ts = 1/sampling_rate

    spectrum = np.fft.fft(signal)/n
    freq = np.fft.fftfreq(n=n, d=Ts)
    
    # slice the first half to display one sided band
    spectrum = np.abs(spectrum)
    i = freq > 0
    spectrum = spectrum[i]
    freq = freq[i]
    
    return spectrum, freq