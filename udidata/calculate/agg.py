import numpy as np
import pandas as pd
from .. import load
from ..dir.utils import get_hours_with_data, data_exists, generate_date_list, get_relevant_hours, get_day_folder_path, get_month_range
from ..utils.df_utils import count_na

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
    
    deg: int or float, default 2.5
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

    # custom agg functions to calculate na count and percentage 
    na_pct = lambda df: df.isna().mean()
    na_count = lambda df: df.isna().sum()

    # group by custom functions
    na_pct = grouped.agg([na_pct]).rename({"<lambda>":"na_pct"}, axis=1)
    na_cnt = grouped.agg([na_count]).rename({"<lambda>":"na_count"}, axis=1)

    # group by regular statistics
    agg = grouped.agg(["mean","median","std","min","max","count"])

    # join all groups and reshape dataframe so it has statistics as index not columns
    agg = agg.join([na_cnt, na_pct]).T.unstack().T

    # rename indices and columns for readability
    agg.columns.names = ["atmos"]
    agg.index.names = ["lat", "lng", "stat"]

    return agg


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
    # verify data exists
    if data_exists(date,hour):
        
        # load data set with one hour data
        df_hour = load.day(date, columns=["lat", "lng"]+cols, hour_range=hour)
    
        # in case load.day return None
        if isinstance(df_hour, pd.DataFrame):

            return spatial_agg(df_hour)

    else:
        pass


#######################################################################################################################

def hourly_spatial_agg(date, hour_range=(0,23), cols=["temperature", "pressure", "humidity", "magnetic_tot"]):
    """
    For a certain date, get hourly aggregations and count for the desired columns. For available hours.

    Parameters
    ----------
    hour_range: int or tuple of int, default (0,23)
        Range of hours of the day to return
    """
    
    relevant_hours = get_relevant_hours(date, hour_range, return_type="int")
    
    # list of tuples of dataframes with hour agg and count data
    hour_dfs = [spatial_hour_agg(date, h, cols) for h in relevant_hours]
    
    # create an index of given hours, for concatanation
    hour_idx = pd.Index(np.array(relevant_hours, dtype=np.int32), name="hour")
    
    # concat all hour_dfs to one df
    agg = pd.concat(hour_dfs, keys=hour_idx)
    
    return agg


#######################################################################################################################

def monthly_spatial_agg(year, month):
    
    """
    """
    dates = get_month_range(year, month)
    
    aggs = []


    # load daily agg data for each day, store in lists
    for date in dates:

        # load agg data and append to aggs list
        path_start = f"{get_day_folder_path(date)}{date.replace('/','')}_"

        agg = pd.read_csv(f"{path_start}daily_agg.csv.gz", index_col=["lat", "lng", "stat"])

        aggs.append(agg)


    # concat the list into one unified dataframe for the entire month
    agg = pd.concat(aggs, axis=1, keys=dates)
    agg.columns.names = ["date", "atmos"]

    
    # extract mean and count data
    mean = agg.xs("mean", level="stat")
    count = agg.xs("count", level="stat")


    # perform aggregations
    total_count = count.sum(axis=1, level="atmos")    # number of data points in the whole month
    wa = (mean * count).sum(axis=1, level="atmos") / total_count    # weighted average
    total_days = mean.count(axis=1, level="atmos")
    std_ = mean.std(axis=1, level="atmos")
    min_ = mean.min(axis=1, level="atmos")
    max_ = mean.max(axis=1, level="atmos")
    med_ = mean.median(axis=1, level="atmos")


    # concat all stats into one data frame and store it
    monthly_agg = pd.concat([wa, std_, min_, max_, med_, total_count, total_days], 
                                    axis=1, 
                                    keys=["mean", "std", "min", "max", "median", "count", "days"], 
                                    names=["stat"])


    # reshape
    monthly_agg = monthly_agg.swaplevel(axis=1).T.unstack().T

    return monthly_agg


#######################################################################################################################

def yearly_spatial_agg(year):
    
    """
    """
    
    # iterate over 12 months of the year and load monthly agg data
    aggs = [load.agg.month(year, month) for month in range(1,13)]
    
    # concat all into one dataframe
    agg = pd.concat(aggs, axis=1, keys=range(1,13), names=["month"])

    # extract mean, count and days data
    mean = agg.xs("mean", level="stat")
    count = agg.xs("count", level="stat")
    days = agg.xs("days", level="stat")

    # perform aggregations
    total_count = count.sum(axis=1, level="atmos")    # number of data points in the whole month
    wa = (mean * count).sum(axis=1, level="atmos") / total_count    # weighted average
    total_days = days.sum(axis=1, level="atmos")
    std_ = mean.std(axis=1, level="atmos")
    min_ = mean.min(axis=1, level="atmos")
    max_ = mean.max(axis=1, level="atmos")
    med_ = mean.median(axis=1, level="atmos")

    # concat all stats into one data frame and store it
    yearly_agg = pd.concat([wa, std_, min_, max_, med_, total_count, total_days], 
                                    axis=1, 
                                    keys=["mean", "std", "min", "max", "median", "count", "days"], 
                                    names=["stat"])


    # reshape
    yearly_agg = yearly_agg.swaplevel(axis=1).T.unstack().T


    return yearly_agg

    
    
    # # concat all stats into one data frame and store it
    # anual_pressure_stats = pd.concat([wa, std, min_, max_, med, total_count, total_days, total_months], 
    #                               axis=1, 
    #                               keys=["mean", "std", "min", "max", "median", "count", "days", "months"])
    
    # return anual_pressure_stats