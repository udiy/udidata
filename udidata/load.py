from pathlib import Path
import glob
import pandas as pd
from .settings import DATA_DIR, COMPRESSION, EXTENSION


#######################################################################################################################

def day(date):
    """
    Returns a pandas DataFrame of daily data

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd

    Returns
    -------
    df : a concatanated pandas Dataframe
    """

    folder_name = f"{DATA_DIR}/{date}"
    csv_files = get_csv(folder_name)
    df = construct_dataframe(csv_files)
    
    return df

#######################################################################################################################

def get_csv(folder_name):
    """
    Returns a list of csv file names

    Parameters
    ----------
    folder_name : str 
        Exact path to folder where daily data is stored

    Returns
    -------
    list_of_csv_files : list of str
    """

    csv_files = [str(filename) for filename in Path(folder_name).glob(f"*.{EXTENSION}")]
    return csv_files


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

    dfs = [pd.read_csv(file, header=None, compression=COMPRESSION) for file in csv_files]
    df = pd.concat(dfs, ignore_index=True)

    return df