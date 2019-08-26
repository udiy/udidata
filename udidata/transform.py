import numpy as np
import pandas as pd
import xarray as xr
from . import load

#######################################################################################################################

def discretize_latlng(df, deg=2.5, lat_col="lat", lng_col="lng"):
    """
    Takes in a DataFrame with latitude and longitude data as a continuous variable and tranfroms it to a discrete variable

    Parameters
    ----------
    df : pd.DataFrame 
        padnas DataFrame with columns for latitude and longitude
    
    deg : int or or float, default 2.5
        Spatial degree interval for for latitude and longitude data

    lat_col : str, default "lat"
        Name of column with latitude data
    
    lng_col : str, default "lng"
        Name of column with longitude data

    Returns
    -------
    df_discrete : pandas Dataframe
        DataFrame with discrete latitude and longitude values
    """

    # discretize lat, lng values into categories using cut method from pandas
    lat_cat = pd.cut(df[lat_col], bins=np.arange(-90,91,deg), labels=np.arange(-90,90,deg)).rename("lat_cat").astype(np.float)
    lng_cat = pd.cut(df[lng_col], bins=np.arange(-180,181,deg), labels=np.arange(-180,180,deg)).rename("lng_cat").astype(np.float)
    df_discrete = pd.concat([df.drop([lat_col,lng_col], axis=1), lat_cat, lng_cat], axis=1)
    
    return df_discrete

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