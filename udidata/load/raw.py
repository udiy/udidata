import os
import numpy as np
import pandas as pd
from ..settings import DATA_DIR, COMPRESSION, EXTENSION, COL_NAMES
from ..dir.utils import get_day_folder_path, data_exists, generate_date_list, get_relevant_hours


#######################################################################################################################

def day(date, columns=COL_NAMES.values(), hour_range=(0,23), where=None, dropna=None):
    
    """
    Returns a pandas DataFrame of daily raw data

    Parameters
    ----------
    date: str 
        Expected date format is yyyy/mm/dd
    
    hour_range: int or tuple of int, default (0,23)
        Range of hours of the day to return

    columns: list of str, default all columns
        Columns to return

    where: dict, default None
        A dictionary of column names and the values to filter by, the dataframe is filtered to accomodate all conditions.
        Meaning cond1 AND cond2 are to be met not cond1 OR cond2

    dropna: str or array-like
        If string there are two options ‘any’, ‘all’.
        If array-like, it takes in column names to drop by

    Returns
    -------
    df: a concatanated pandas Dataframe
    """

    if data_exists(date):

        # get relevant hours to query for the date
        relevant_hours = get_relevant_hours(date, hour_range)

        if len(relevant_hours) == 0:
            print("No data for desired hours.")
            return

        # create a list of relevant csv files
        folder_path = get_day_folder_path(date)
        csv_files = [f"{folder_path}/{h}.{EXTENSION}" for h in relevant_hours]

        # construct csv file
        df = construct_day_df(csv_files, columns, dropna, where)
        if df.empty:
            print(f"On {date} no data matched your critiriea, try changing your where/na filters")
        return df
        
    else:
        print(f"No data at all for {date}")
        return
    

#######################################################################################################################

def days(date_range, columns=COL_NAMES.values(), hour_range=(0,23), where=None, dropna=None):
    """
    Returns a pandas DataFrame of data between specified dates

    Parameters
    ----------
    date_range : array-like of str
        A tuple in the form of (start_date, end_date). Dates must be in the following format: yyyy/mm/dd
    
    dropna : str or array-like
        If string there are two options ‘any’, ‘all’.
        If array-like, it takes in column names to drop by
    """

    str_dates = generate_date_list(*date_range)

    # load dataframes from the wanted dates and put them in a list
    dfs = [day(date, columns, hour_range, where, dropna) for date in str_dates]
    
    # make sure all entries in dfs are of type DataFrame before concatanation
    dfs = list(filter(lambda x: isinstance(x, pd.DataFrame),dfs))
    
    if len(dfs) > 0:
        df = pd.concat(dfs,ignore_index=True)
        return df
    else:
        print(f"Sorry, no data found for these dates: {date_range[0]} to {date_range[-1]}")


#######################################################################################################################

def construct_day_df(csv_files, columns, dropna, where):
    """
    Returns pandas DataFrame

    Parameters
    ----------
    csv_files : list of str 
        A list with exact path to csv files to be concatanated

    columns : list of str
        Columns to return
    
    dropna : str or array-like
        If string there are two options ‘any’, ‘all’.
        If array-like, it takes in column names to drop by
    
    where : dict, default None
        A dictionary of column names and the values to filter by, the dataframe is filtered to accomodate all conditions.
        Meaning cond1 AND cond2 are to be met not cond1 OR cond2

    Returns
    -------
    df : pandas DataFrame
    """

    dfs = [pd.read_csv(file, usecols=columns, compression=COMPRESSION)[columns] for file in csv_files]
    dfs = [df for df in dfs if isinstance(df, pd.core.frame.DataFrame)]   # make sure all entries in dfs are of type DataFrame before concatanation
    df = pd.concat(dfs, ignore_index=True)

    if isinstance(dropna, str) and dropna in ["any", "all"]:
        df.dropna(how=dropna, inplace=True)
    elif isinstance(dropna, (list, tuple)):
        df.dropna(subset=dropna, inplace=True)

    if where is not None:
        for col in where:
            llim, ulim = where[col]
            df = df[df[col].between(llim, ulim)]

    return df