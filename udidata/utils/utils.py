import os

from ..settings import DATA_DIR


#######################################################################################################################

def data_exists(date):
    """
    Checks if there is a directory with data files for given date

    Parameters
    ----------
    date : str 
        Expected date format is yyyy/mm/dd

    Returns
    -------
    bool
    """
    
    file_path = f"{DATA_DIR}/{date}"
    if os.path.exists(file_path):
        return True
    return False
