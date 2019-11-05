import numpy as np
import pandas as pd
import xarray as xr
from . import load, utils

#######################################################################################################################

def convert_agg_dataset(date):
    """ 
    For a given date turn dataframe of aggregated data into xarray dataset

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd
    
    Returns
    -------
    ds : xarray Dataset
        Dataset with 3 dimensions latitude, longitude and statistic
    """
    atmos_props = ["pressure", "temperature", "humidity", "magnetic_tot"]
    dfs = {atmos_prop:load.agg.day(date, atmos_prop) for atmos_prop in atmos_props}
    das = {}

    for atmos_prop in dfs:
        df = dfs[atmos_prop]
        cols = [col for col in df]

        # make df into a series with multiindex with 3 levels
        s = pd.concat([df[col] for col in cols], keys=cols, names=("stat", "lat", "lng"))

        da = xr.DataArray.from_series(s)
        da.name = atmos_prop

        das[atmos_prop] = da

    ds = xr.Dataset(data_vars=das)
    return ds

#######################################################################################################################

def unified_dataset(date_range):
    """
    Create an xarray dataset holding all the data within specified date range.
    For given date range transform all of its daily agg data into xarray datasets, then unify them into one big dataset.
    
    Parameters
    ----------
    date_range : array-like of str
        A tuple in the form of (start_date, end_date). Dates must be in the following format: yyyy/mm/dd
        
    Returns
    -------
    ds : xarray Dataset
        A concatanated xarray Dataset holding all the data between specified date range
    """
    start_date = date_range[0]
    end_date = date_range[-1]
    str_dates = [str(d.date()).replace("-","/") for d in pd.date_range(start=start_date, end=end_date)]
    str_dates = [date for date in str_dates if utils.utils.data_exists(date)]    # remove dates with no data

    dss = [convert_agg_dataset(date) for date in str_dates]    # create a list of xr.Datasets to concat along date dimension
    date_idx = pd.Index(str_dates, name="date")    # create an index of dates
    ds = xr.concat(dss, dim=date_idx)
    return ds

#######################################################################################################################

def pivot_dataset(ds, prop="pressure", stat="mean"):
    """
    Takes in xarray dataset of aggregated data and return a pandas DataFrame after pivotting. Location as index and date as columns.

    Parameters
    ----------
    ds : xarray Dataset
        A dataset of aggregated data with a specified format

    prop : {'pressure', 'temperature', 'humidity', 'magnetic_tot'}, default 'pressure'
        Atmospheric property of interest
        
    stat : {'count', ' mean', ' median', ' std', ' min', ' max'}, default 'count'
        A statistic of interest to show on the plot.

    Returns
    -------
    df : pandas DataFrame
        A pivotted dataframe
    """
    da = ds.sel(stat=stat)[prop]
    df = da.to_dataframe(name=stat).drop(["stat"], axis=1)
    df = df.dropna().reset_index().set_index(["lat","lng"])
    df = df.pivot(columns="date")
    return df
