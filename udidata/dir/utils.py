import os
import pandas as pd
from ..settings import DATA_DIR


#######################################################################################################################

def iterate_days(dates, task):
    
    """ 
    Iterate over day folders in c_data2 and execute task for each day.
    
    Parameters
    ----------
    dates : array-like of str
        Start date and end date of days to iterate over. 
        A date is a string in a format of yyyy/mm/dd.
        If only one day is desried pass and array with one element
        
    task : function
        A function to execute for each day folder. For example read all csv files.
        Its first argument should be date (as a string) (see below)
        
    Return
    ------
    tasks_returns : list
        A list of the return values for each call of task
    """
    
    # check types
    if not isinstance(dates, (list, tuple)):
        raise TypeError(f"Parameter dates can't be of type {type(dates)}")
        
    if not callable(task):
        raise TypeError("task must be a function")
    
    # create a list of dates
    start_date = dates[0]
    end_date = dates[-1]
    date_range = pd.date_range(start_date, end_date, freq="D")
    
    tasks_returns = [task(date.strftime("%Y/%m/%d")) for date in date_range]
    return tasks_returns
            

#######################################################################################################################

def get_day_folder_path(date):
    
    """
    Parameters
    ----------
    date : str
        Date in the format of yyyy/mm/dd
        
    Returns
    -------
    day_folder_path : str
        Path for folder containing daily data
    """
    
    return f"{DATA_DIR}/{date}/"