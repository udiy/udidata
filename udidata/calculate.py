from . import load, transform
import pandas as pd

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
        df_discrete = transform.discretize_latlng(df, deg=deg)

        # create a groupby object grouped by lat, lng categories
        grouped = df_discrete.groupby(by=["lat_cat","lng_cat"])
        data_count = grouped.size().rename(("count","count"))    # name as a tuple to ease concatanation later on
        data_agg = grouped.agg(["mean","median","std","min","max"])
        df_agg = pd.concat([data_count, data_agg], axis=1)

        return df_agg