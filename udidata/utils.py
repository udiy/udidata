import os
import numpy as np
import pandas as pd
import xarray as xr

from .settings import DATA_DIR


#######################################################################################################################

def reindex_utc(self, time_col="raw_time", drop=False):
    """
    Parameters
    ----------
    self : pandas DataFrame
        Dataframe with raw time column

    time_col : str, default 'raw_time'
        Column name that holds raw time data
    
    drop : bool, default False
        If true, original raw time column will be dropped for DataFrame

    Returns
    -------
    self : pandas DataFrame
        Dataframe with time as index
    """

    self.index = pd.to_datetime(self[time_col], unit="ms")
    self.index.name = "utc"

    if drop:
        self = self.drop([time_col], axis=1)

    return self


pd.DataFrame.reindex_utc = reindex_utc

#######################################################################################################################

def count_na(self):
    
    """ 
    Count nan values in self on every column
    """
    num_of_values = self.count().rename("values")    # number of values (not NaN) in each column
    num_of_nan = self.isna().sum().rename("nan")    # number of NaN values in each column
    nan_pct = self.isna().mean().rename("nan_pct")
    
    return pd.concat([num_of_values, num_of_nan, nan_pct], axis=1)


pd.DataFrame.count_na = count_na

#######################################################################################################################

def data_exists(date):
    """
    Checks if there is a directory with data files for given date

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd

    Returns
    -------
    bool
    """
    
    file_path = f"{DATA_DIR}/{date}"
    if os.path.exists(file_path):
        return True
    return False

#######################################################################################################################

def scale_column(self, col, func=np.log10):
    """
    Scale a column of DataFrame self, and return new DataFrame with new column
    
    Parameters
    ----------
    self : pd.DataFrame 
        padnas DataFrame

    col : str
        Column name to scale

    func : ufunc, default np.log10
        Function to use for scaling

    Returns
    -------
    self : pandas Dataframe
        DataFrame with scaled column
    """
    s_col = self[col]    # var to hold col as pandas Series
    self[f"scaled_{col}"] = func(s_col)    # create a new scaled column and inset to self
    return self
    
pd.DataFrame.scale_column = scale_column

#######################################################################################################################

def discretize_latlng(self, deg=2.5, lat_col="lat", lng_col="lng", drop=True):
    """
    Takes in a DataFrame with latitude and longitude data as a continuous variable and tranfroms it to a discrete variable

    Parameters
    ----------
    self : pd.DataFrame 
        padnas DataFrame with columns for latitude and longitude
    
    deg : int or or float, default 2.5
        Spatial degree interval for for latitude and longitude data

    lat_col : str, default "lat"
        Name of column with latitude data
    
    lng_col : str, default "lng"
        Name of column with longitude data

    drop : bool, default True
        If true, original latitude and logitude columns will be dropped for DataFrame

    Returns
    -------
    self : pandas Dataframe
        DataFrame with discrete latitude and longitude values
    """

    # discretize lat, lng values into categories using cut method from pandas
    self["lat_cat"] = pd.cut(self[lat_col], bins=np.arange(-90,91,deg), labels=np.arange(-90,90,deg))
    self["lng_cat"] = pd.cut(self[lng_col], bins=np.arange(-180,181,deg), labels=np.arange(-180,180,deg))

    if drop:
        self = self.drop([lat_col, lng_col], axis=1)
    
    return self

pd.DataFrame.discretize_latlng = discretize_latlng

#######################################################################################################################

def zip_columns(self, columns, drop=True, new_col=None):
    """
    Zip two (or more) columns into one column
    
    Parameters
    ----------
    self : pd.DataFrame 
        padnas DataFrame

    colums : array-like
        Columns to zip into one column

    drop : bool, default True
        If true, original latitude and logitude columns will be dropped for DataFrame

    new_col : str, default None
        New concatenated column name. If left None, new name will be a string concatanation of column names

    Returns
    -------
    self : pandas Dataframe
        DataFrame
    """

    if isinstance(new_col,str):
        col_name = new_col
    else:
        col_name = "".join(columns)

    self[col_name] = list(zip(*[self[col] for col in columns]))

    if drop:
        self = self.drop(columns, axis=1)

    return self
    
pd.DataFrame.zip_columns = zip_columns

#######################################################################################################################

def filter_ds(self, by, gt=1):
    """
    Filter dataset by condition that reduce date dimension

    Parameters
    ----------
    self : xarray Dataset
        A dataset of aggregated data with a specified format

    by : {'total count', 'total days'}
        'total count' - filter dataset by total count (sum) greater than
        'total days' - filter dataset by total count of not-nan values greater than
        
    gt : int, default 0
        Greater than. Minimal number for condition to be True

    Returns
    -------
    ds : xarray Dataset
        Filtered Dataset
    """
    if by.lower()=="total count":
        da = self.sel(stat="count")["pressure"].sum(dim="date")
        ds = self.where(da >= gt).dropna(dim="lat", how="all").dropna(dim="lng", how="all")
    elif by.lower()=="total days":
        da = self.sel(stat="count")["pressure"].count(dim="date")
        ds = self.where(da >= gt).dropna(dim="lat", how="all").dropna(dim="lng", how="all")
    else:
        print("Your dataset wasn't filtered")
        return self
        
    return ds
    
xr.Dataset.filter_ds = filter_ds

#######################################################################################################################

def get_stats(self):
    """
    Get basic statistics about data in dataset. Total days and total count.
    """
    da1 = self.sel(stat="count")["pressure"].sum(dim="date")
    s1 = da1.where(da1>0).to_series().rename("total count").dropna()
    da2 = self.sel(stat="count")["pressure"].count(dim="date")
    s2 = da2.where(da2>0).to_series().rename("total days").dropna()
    df_total = pd.concat([s1, s2], axis=1)
    return df_total.sort_values(by="total days", ascending=False)

xr.Dataset.get_stats = get_stats