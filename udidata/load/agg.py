from ..dir.utils import DATA_DIR, add_lead_zero, get_day_folder_path
import pandas as pd
import xarray as xr

#######################################################################################################################

# colum names
atmos = ["pressure", "temperature", "humidity", "magnetic_tot"]
idx = ["lat", "lng", "stat"]

def load_agg(path, atmos=atmos, idx=idx):
    """
    Loads an aggregated dataframe (specific format) from path
    
    Parameters
    ----------
    path: str
        Path to dataframe to be loaded

    atmos: array-like, default ["pressure", "temperature", "humidity", "magnetic_tot"]
        All atmospheric propeties wished to retrieve

    Returns
    -------
    agg: pandas DataFrame
    """

    agg = pd.read_csv(path, index_col=idx, usecols=idx+atmos)
    agg.columns.names = ["atmos"]
    
    return agg


#######################################################################################################################

def day(date, atmos=atmos):
    
    """
    Returns a dataframe of daily aggregated data

    Parameters
    -------
    date: str
        Format yyyy/mm/dd
    """
    path = f"{get_day_folder_path(date)}{date.replace('/','')}_daily_agg.csv.gz"
    
    return load_agg(path, atmos)


#######################################################################################################################

def hourly(date, atmos=atmos):
    
    """
    Returns a dataframe of hourly aggregated data for a specific date

    Parameters
    -------
    date: str
        Format yyyy/mm/dd
    """
    path = f"{get_day_folder_path(date)}{date.replace('/','')}_hourly_agg.csv.gz"
    return load_agg(path, atmos, idx=["hour"]+idx)


#######################################################################################################################

def month(year, month, atmos=atmos):
    
    """
    Returns a dataframe of monthly aggregated data

    Parameters
    ----------
    year: int or str
        Format yyyy
    
    month: int or str
        Format mm
    """
    
    # construct path for a month data folder
    month = add_lead_zero(month)
    path = f"{DATA_DIR}/{year}/{month}/{year}{month}_monthly_agg.csv.gz"

    return load_agg(path, atmos)
    

#######################################################################################################################

def year(year, atmos=atmos):
    """
    Returns a dataframe of yearly aggregated data
    
    Parameters
    ----------
    year : str or int
        Format yyyy
    """

    path = f"{DATA_DIR}/{year}/{year}_yearly_agg.csv.gz"
    return load_agg(path, atmos)


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
