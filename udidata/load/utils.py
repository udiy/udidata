import numpy as np
from collections.abc import Iterable
from ..dir.utils import get_day_folder_path, data_exists, get_hours_with_data, add_lead_zero

#######################################################################################################################

def is_numeric(a):
    
    """
    Check if parameter a can be converted to int
    """
    try:
        int(a)
        return True
    except:
        return False

#######################################################################################################################

def generate_hour_list(hour_range):
    
    """
    Takes in an hour_range and returns all hours in a list generator.
    
    Parameters
    ----------
    hour_range: array-like or int
        Desired hours
    """

    if isinstance(hour_range, Iterable):

        # validate hour_range input
        if len(hour_range) > 2:
            raise ValueError(f"hour_range have more than 2 arguemnts. It should be like this (start_hour, end_hour).")

        if not all(map(is_numeric, hour_range)):
            raise TypeError("hour_range entries must be numbers.")

        if not all(map(lambda x: x<24, hour_range)):
            raise ValueError("hour_range entries must be in the range of 0-23")

        # unpack values
        start_hour = hour_range[0]
        end_hour = hour_range[-1]

    else:

        # validate hour_range input
        if not is_numeric(hour_range):
            TypeError("hour_range entries must be numbers.")

        if hour_range>23:
            raise ValueError("hour_range entries must be in the range of 0-23")

        start_hour = end_hour = hour_range


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