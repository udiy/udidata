import os
from pathlib import Path
import glob
import pandas as pd
from .settings import DATA_DIR, COMPRESSION, EXTENSION


#######################################################################################################################

def day(date, hour_range=(0,23)):
    """
    Returns a pandas DataFrame of daily data

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd
    
    hour_range : int or tuple of int, default (0,23)
        Range of hours of the day for querying data

    Returns
    -------
    df : a concatanated pandas Dataframe
    """

    folder_name = f"{DATA_DIR}/{date}"
    csv_files, no_data = get_csv(folder_name, hour_range)
    if no_data != []:
        print(f"On {date} no data for the following hours {no_data}")
    if csv_files != []:
        df = construct_dataframe(csv_files)
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

def construct_dataframe(csv_files):
    """
    Returns pandas DataFrame

    Parameters
    ----------
    csv_files : list of str 
        A list with exact path to csv files to be concatanated

    Returns
    -------
    df : pandas DataFrame
    """

    dfs = [pd.read_csv(file, compression=COMPRESSION) for file in csv_files]
    df = pd.concat(dfs, ignore_index=True)

    return df