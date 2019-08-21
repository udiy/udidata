import pandas as pd


#######################################################################################################################

def reindex_utc(self):
    """
    """

    self.index = pd.to_datetime(self["raw_time"], unit="ms")
    self.index.name = "utc"

    return self


pd.DataFrame.reindex_utc = reindex_utc

#######################################################################################################################

def count_na(self):
    
    """ count nan values in a given df on every column
    """
    num_of_values = self.count().rename("values")    # number of values (not NaN) in each column
    num_of_nan = self.isna().sum().rename("nan")    # number of NaN values in each column
    num_of_rows = self.shape[0]
    nan_pct = (num_of_nan / num_of_rows).rename("nan_pct")
    
    print(f"Total number of rows: {num_of_rows}")
    return pd.concat([num_of_values, num_of_nan, nan_pct], axis=1)


pd.DataFrame.count_na = count_na

#######################################################################################################################