import numpy as np
import pandas as pd
from . import load, utils

#######################################################################################################################

def spatial_agg(df, deg=2.5): 
    """
    For a given df calculate aggregation (count, mean, median, std, min, max) 
    for data variables (temperature, pressure, humidity, magnetic_tot)
    grouped by latitude and longitude category

    Parameters
    ----------
    df : pandas DataFrame
        Pandas dataframe with data for the desired sampling range (hourly, daily)
    
    deg : int or or float, default 2.5
        Spatial degree interval for for latitude and longitude data
    
    Returns
    -------
    data_agg : pandas DataFrame
        DataFrame with aggregated data for every atmospheric variable

    data_count : pandas Series
        Series with count of data points for every location
    """
    # Group data points by lat, lng categories
    df = df.discretize_latlng(deg=deg)

    # create a groupby object grouped by lat, lng categories
    grouped = df.groupby(by=["lat_cat","lng_cat"])

    # get count of data points (group size) for each group
    data_count = grouped.size().rename("count")

    # group by these statistics
    data_agg = grouped.agg(["mean","median","std","min","max"])

    # rename indices and columns for readability
    data_agg.columns.names = ["atmos","stat"]
    data_agg.index.names = ["lat", "lng"]
    data_count.index.names = ["lat", "lng"]

    # reshape dataframe so it has statistics as index not columns
    data_agg = data_agg.T.unstack().T
    

    return data_agg, data_count


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