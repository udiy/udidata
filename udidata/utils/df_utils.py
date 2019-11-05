import numpy as np
import pandas as pd

#######################################################################################################################

def to_utc(self, time_col="raw_time", reindex=False, drop=False):
    """
    Parameters
    ----------
    self : pandas DataFrame
        Dataframe with raw time column

    time_col : str, default 'raw_time'
        Column name that holds raw time data

    reindex : bool, default False
        If True, use UTC time as index

    drop : bool, default False
        If true, original raw time column will be dropped for DataFrame

    Returns
    -------
    self : pandas DataFrame
        Dataframe with time as index
    """
    if time_col in self.columns:
        df = self.copy()
        utc_col = pd.to_datetime(df[time_col], unit="ms")

        if reindex:
            df.index = utc_col
            df.index.name = "utc"
        else:
            df["utc"] = utc_col

    else:
        raise KeyError("There's no time column in your dataframe!")

    if drop:
        df = df.drop([time_col], axis=1)

    return df


pd.DataFrame.to_utc = to_utc

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
    df = self.copy()
    s_col = df[col]    # var to hold col as pandas Series
    df[f"scaled_{col}"] = func(s_col)    # create a new scaled column and inset to self
    return df
    
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
    df = self.copy()

    # discretize lat, lng values into categories using cut method from pandas
    df["lat_cat"] = pd.cut(df[lat_col], bins=np.arange(-90,91,deg), labels=np.arange(-90,90,deg))
    df["lng_cat"] = pd.cut(df[lng_col], bins=np.arange(-180,181,deg), labels=np.arange(-180,180,deg))

    if drop:
        df = df.drop([lat_col, lng_col], axis=1)
    
    return df

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

    df = self.copy()

    if isinstance(new_col,str):
        col_name = new_col
    else:
        col_name = "".join(columns)

    df[col_name] = list(zip(*[df[col] for col in columns]))

    if drop:
        df = df.drop(columns, axis=1)

    return df
    
pd.DataFrame.zip_columns = zip_columns

