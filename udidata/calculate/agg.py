import numpy as np
import pandas as pd
from .. import load
from ..dir.utils import get_hours_with_data, data_exists, generate_date_list, get_relevant_hours

#######################################################################################################################

def spatial_agg(df, deg=2.5): 
    """
    For a given df calculate aggregation (count, mean, median, std, min, max) 
    for data variables (temperature, pressure, humidity, magnetic_tot)
    grouped by latitude and longitude category

    Parameters
    ----------
    df: pandas DataFrame
        Pandas dataframe with data for the desired sampling range (hourly, daily)
    
    deg: int or or float, default 2.5
        Spatial degree interval for for latitude and longitude data
    
    Returns
    -------
    data_agg: pandas DataFrame
        DataFrame with aggregated data for every atmospheric variable

    data_count: pandas Series
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

def spatial_hour_agg(date, hour, cols=["temperature", "pressure", "humidity", "magnetic_tot"]):
    """
    Get spatial aggregations for a specific hour in a specific date.

    Parameters
    ----------
    date: str
        Format yyyy/mm/dd

    hour: str or int
        Range 0-23
    
    Returns
    -------
    data_agg: pandas DataFrame
        DataFrame with aggregated data for every atmospheric variable

    data_count: pandas Series
        Series with count of data points for every location
    """
    # load data set with one hour data
    df_hour = load.day(date, columns=["lat", "lng"]+cols, hour_range=hour)
    
    # in case load.day return None
    if isinstance(df_hour, pd.DataFrame):
        # drop rows where all variables are nan
        df_hour = df_hour.dropna(how="all", subset=cols)

        # make this df a ds with dimensions: location, atmos prop, statistic
        return spatial_agg(df_hour)


#######################################################################################################################

def hourly_spatial_agg(date, hour_range=(0,23), cols=["temperature", "pressure", "humidity", "magnetic_tot"]):
    """
    For a certain date, get hourly aggregations and count for the desired columns. For available hours.

    Parameters
    ----------
    hour_range: int or tuple of int, default (0,23)
        Range of hours of the day to return
    """
    
    relevant_hours = get_relevant_hours(date, hour_range)
    
    # list of tuples of dataframes with hour agg and count data
    hour_dfs = [spatial_hour_agg(date, h, cols) for h in relevant_hours]
    
    # spilt the tuples to two list of hourly agg data and hourly count data
    agg = [data[0] for data in hour_dfs]
    count = [data[1] for data in hour_dfs]
    
    # create an index of given hours, for xarray concatanation
    hour_idx = pd.Index(np.array(relevant_hours, dtype=np.int32), name="hour")
    
    agg_df = pd.concat(agg, keys=hour_idx)
    count_df = pd.concat(count, keys=hour_idx)
    
    joined_df = agg_df.join(count_df)
    
    return joined_df