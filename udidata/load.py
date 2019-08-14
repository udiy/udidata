import os
import pandas as pd
from .settings import DATA_DIR, COMPRESSION, EXTENSION, COL_NAMES


#######################################################################################################################

def day(date, columns=COL_NAMES.values(), hour_range=(0,23), where=None, dropna=False):
    """
    Returns a pandas DataFrame of daily data

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd
    
    hour_range : int or tuple of int, default (0,23)
        Range of hours of the day to return

    columns : list of str, default all columns
        Columns to return

    where : dict, default None
        A dictionary of column names and the values to filter by, the dataframe is filtered to accomodate all conditions.
        Meaning cond1 AND cond2 are to be met not cond1 OR cond2

    dropna : bool, default False
        If True, drops rows that has at least one NaN value in them
        It can also take a list or a tuple of column names to drop by

    Returns
    -------
    df : a concatanated pandas Dataframe
    """

    folder_name = f"{DATA_DIR}/{date}"
    csv_files, no_data = get_csv(folder_name, hour_range)
    if no_data != []:
        print(f"On {date} no data for the following hours {no_data}")
    if csv_files != []:
        df = construct_dataframe(csv_files, columns, dropna, where)
        if df.empty:
            print("No data matched your critiriea, try changing your filters")
        return df
    else:
        print(f"No data for {date}")
        return 
    

#######################################################################################################################

def get_csv(folder_name, hour_range):
    """
    Returns a list of csv file names

    Parameters
    ----------
    folder_name : str 
        Exact path to folder where daily data is stored
    
    hour_range : int or tuple of int, default (0,23)
        Range of hours of the day for querying data

    Returns
    -------
    list_of_csv_files : list of str
    """

    no_data = []    # store hours that have no data files
    csv_files = []

    start_hour = int(hour_range[0])
    end_hour = int(hour_range[-1])

    for h in range(start_hour, end_hour + 1):
        # construct the file path for every hour
        if h in range(0,10):
            h = f"0{int(h)}"
        file_path = f"{folder_name}/{h}.{EXTENSION}"
        if os.path.exists(file_path):
            csv_files.append(file_path)
        else:
            no_data.append(int(h))

    return csv_files, no_data


#######################################################################################################################

def construct_dataframe(csv_files, columns, dropna, where):
    """
    Returns pandas DataFrame

    Parameters
    ----------
    csv_files : list of str 
        A list with exact path to csv files to be concatanated

    columns : list of str
        Columns to return
    
    dropna : bool or array-like
        If True, drops rows that has at least one NaN value in them.
        It can also take a list or a tuple of column names to drop by
    
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

    if dropna is True:
        df.dropna(inplace=True)
    elif isinstance(dropna, (list, tuple)):
        df.dropna(subset=dropna, inplace=True)

    if where is not None:
        for col in where:
            llim, ulim = where[col]
            df = df[df[col].between(llim, ulim)]

    return df