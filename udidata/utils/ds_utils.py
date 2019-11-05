import pandas as pd
import xarray as xr

#######################################################################################################################

def filter_ds(self, by, gt=1):
    """
    Filter dataset by condition that reduce date dimension

    Parameters
    ----------
    self : xarray Dataset
        A dataset of aggregated data with a specified format

    by : {'total count', 'total days'}
        'total count' - filter dataset by total count (sum) greater than
        'total days' - filter dataset by total count of not-nan values greater than
        
    gt : int, default 0
        Greater than. Minimal number for condition to be True

    Returns
    -------
    ds : xarray Dataset
        Filtered Dataset
    """
    if by.lower()=="total count":
        da = self.sel(stat="count")["pressure"].sum(dim="date")
        ds = self.where(da >= gt).dropna(dim="lat", how="all").dropna(dim="lng", how="all")
    elif by.lower()=="total days":
        da = self.sel(stat="count")["pressure"].count(dim="date")
        ds = self.where(da >= gt).dropna(dim="lat", how="all").dropna(dim="lng", how="all")
    else:
        print("Your dataset wasn't filtered")
        return self
        
    return ds
    
xr.Dataset.filter_ds = filter_ds

#######################################################################################################################

def get_stats(self):
    """
    Get basic statistics about data in dataset. Total days and total count.
    """
    da1 = self.sel(stat="count")["pressure"].sum(dim="date")
    s1 = da1.where(da1>0).to_series().rename("total count").dropna()
    da2 = self.sel(stat="count")["pressure"].count(dim="date")
    s2 = da2.where(da2>0).to_series().rename("total days").dropna()
    df_total = pd.concat([s1, s2], axis=1)
    return df_total.sort_values(by="total days", ascending=False)

xr.Dataset.get_stats = get_stats