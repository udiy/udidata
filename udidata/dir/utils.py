import os
import numpy as np
import pandas as pd
from ..settings import DATA_DIR, EXTENSION
from ..utils.utils import is_numeric


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
    date_range = generate_date_list(start_date, end_date)
    date_range = filter(data_exists, date_range)
    
    tasks_returns = [task(date) for date in date_range]
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


#######################################################################################################################

def generate_date_list(start_date, end_date):
    
    """
    Creates and returns a list of string dates with the format yyyy/mm/dd.
    Parameter dates should follow that format too!
    
    """
    return [date.strftime("%Y/%m/%d") for date in pd.date_range(start_date, end_date)]


#######################################################################################################################

def data_exists(date):
    """
    Checks if there is a directory with daily data files for given date

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd

    Returns
    -------
    bool
    """
    
    file_path = get_day_folder_path(date)
    if os.path.exists(file_path):
        return True
    return False


#######################################################################################################################

def hour_exists(date, hour):
    
    """
    For a given date and hour, check if data exists.
    
    Parameters
    ----------
    date : str
        Format yyyy/mm/dd
    hour : str or int
        Format hh
    """
    folder_path = get_day_folder_path(date)
    
    # construct full file path
    file_path = f"{folder_path}/{hour}.{EXTENSION}"
    
    # check if file exists
    return os.path.exists(file_path)


#######################################################################################################################

def add_lead_zero(hour):
    
    """
    For representing hour as a string, hour must be in the form of two digits.
    Which means that in the range 0-9, there needs to be a leading zero.
    This function takes in an integer represting an hour, and adds a leading zero if necessary
    
    Parameters
    ----------
    hour: str or int
    """
    if hour in range(10):
        return f"0{hour}"
    return str(hour)


#######################################################################################################################

def get_hours_with_data(date):
    
    """
    For a specific date, return a list of hours it had data.
    """
    # check if data exists at all for this date
    if data_exists(date):
        
        # create a masked array. Indicies with True value are hours with data
        masked_array = [hour_exists(date, h) for h in map(add_lead_zero, range(24))]
        return np.arange(24)[masked_array]
            
    else:
        return []


#######################################################################################################################

def generate_hour_list(hour_range):
    
    """
    Takes in an hour_range and returns all hours in a list generator.
    
    Parameters
    ----------
    hour_range: array-like or int
        Desired hours
    """

    if isinstance(hour_range, (list, tuple)):

        # validate hour_range input
        if len(hour_range) > 2:
            raise ValueError(f"hour_range have more than 2 arguemnts. It should be like this (start_hour, end_hour).")

        if not all(map(is_numeric, hour_range)):
            raise TypeError("hour_range entries must be numbers.")

        if not all(map(lambda x: int(x)<24, hour_range)):
            raise ValueError("hour_range entries must be in the range of 0-23")

        # unpack values
        start_hour = int(hour_range[0])
        end_hour = int(hour_range[-1])

    else:

        # validate hour_range input
        if not is_numeric(hour_range):
            TypeError("hour_range entries must be numbers.")

        if int(hour_range)>23:
            raise ValueError("hour_range entries must be in the range of 0-23")

        start_hour = end_hour = int(hour_range)


    # create desired_hours list
    return range(start_hour, end_hour+1)


#######################################################################################################################

def get_relevant_hours(date, hour_range):

    """
    Parameters
    ----------
    date: str 
        Expected date format is yyyy/mm/dd
    
    hour_range: int or tuple of int, default (0,23)
        Range of desired hours of the day to return
    """

    avail_hours = get_hours_with_data(date)    # get a list of available hours for that day
    desired_hours = generate_hour_list(hour_range)    # get a list of desired hours

    relevant_hours = np.intersect1d(desired_hours, avail_hours)    # list of hours to query - hours that are both desired and available
    no_data_hours = np.setdiff1d(desired_hours, avail_hours)    # list of desired hours that are not available

    if no_data_hours.size > 0:
        print(f"On the {date}, no data for the following hours: {list(no_data_hours)}")

    # add leading zero to conform to the format
    relevant_hours = map(add_lead_zero, relevant_hours)
    
    return list(relevant_hours)

#######################################################################################################################