import numpy as np
import pandas as pd
from . import load, utils

#######################################################################################################################

def daily_spatially_agg(date, deg=2.5): 
    """
    For a given date calculate aggregation (count, mean, median, std, min, max) 
    for data variables (temperature, pressure, humidity, magnetic_tot)
    grouped by latitude and longitude category

    Parameters
    ----------
    date : str
        Expected date format is yyyy/mm/dd
    
    deg : int or or float, default 2.5
        Spatial degree interval for for latitude and longitude data
    
    Returns
    -------
    df_agg : pandas Dataframe
        DataFrame with aggregated data for every variable
    """
    cols = ['lat', 'lng', 'temperature', 'pressure', 'humidity', 'magnetic_tot']
    df = load.day(date, columns=cols, dropna=True)
    
    if isinstance(df, pd.DataFrame):
        # Group data points by lat, lng categories
        df = df.discretize_latlng(deg=deg)

        # create a groupby object grouped by lat, lng categories
        grouped = df.groupby(by=["lat_cat","lng_cat"])
        data_count = grouped.size().rename(("count","count"))    # name as a tuple to ease concatanation later on
        data_agg = grouped.agg(["mean","median","std","min","max"])
        df_agg = pd.concat([data_count, data_agg], axis=1)

        return df_agg

#######################################################################################################################

def fourier_transform(signal, sampling_rate):
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