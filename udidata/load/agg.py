from ..settings import DATA_DIR
import pandas as pd

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

    laglng : tuple of floats, default None
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