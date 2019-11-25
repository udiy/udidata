from ..dir.utils import DATA_DIR, add_lead_zero
import pandas as pd
import xarray as xr

#######################################################################################################################

def day(date, column=None, latlng=None):
    """
    Returns a pandas DataFrame of daily aggregated data

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd

    column : str, default None
        Specify a spcecific column if desried

    latlng : tuple of floats, default None
        Specify specific latitude and longitude if desried
        Expected format is (lat,lng)

    Returns
    -------
    df : an aggregated pandas Dataframe
    """

    df = pd.read_csv(f"{DATA_DIR}/{date}/{date.replace('/','')}_daily_agg.csv.gz", index_col=[0,1], header=[0,1]) 
    df.index.names = ["lat", "lng"]
    df.columns.names = ["atmos", "stat"]
                     
    if column:
        df = df[["count", column]].droplevel(0, axis=1)
    if latlng:
        df = df.loc[[latlng]]
    return df 

#######################################################################################################################

def month(year, month, stats=["mean", "std", "min", "max", "median", "count", "days"]):
    
    """
    Load agg monthly data, if saved as csv.

    Parameters
    ----------
    year : int or str
        Format yyyy
    month : int or str
        Format mm

    Returns
    -------
    df : an aggregated pandas Dataframe
    """
    
    # construct path for a month data folder
    month = add_lead_zero(month)
    path = f"{DATA_DIR}/{year}/{month}/{year}{month}_monthly_pressure_agg.csv.gz"

    # load monthly agg data
    latlng = ["lat", "lng"]
    df = pd.read_csv(path, index_col=latlng, usecols=latlng+stats)
    return df

#######################################################################################################################

def year(year, stats=["mean", "std", "min", "max", "median", "count", "days", "months"]):
    """
    Returns an xarray Dataset of yearly aggregated data
    
    Parameters
    ----------
    year : str or int
        Format yyyy

    Returns
    -------
    df : an aggregated xarray Dataset
    """


    path = f"{DATA_DIR}/{year}/{year}_anual_pressure_agg.csv.gz"

    latlng = ["lat", "lng"]
    df = pd.read_csv(path, index_col=latlng, usecols=latlng+stats)
    return df

#######################################################################################################################

def years(year_range):
    """
    Returns a concatanated xarray Dataset of yearly aggregated data for specified year range.
    The range is inclusive, for example, for [2014,2016] it will return data for 2014, 2015 and 2016
    
    Parameters
    ----------
    year_range : array-like of int
        Expected year format is yyyy

    Returns
    -------
    df : an aggregated xarray Dataset
    """

    start_year = year_range[0]
    end_year = year_range[-1] + 1
    load_year = year    # more indicative name, and preventing name collision in the next line
    dss = [load_year(year) for year in range(start_year,end_year)]    # list of yearly datasets
    ds = xr.concat(dss, dim="date")
    return ds
