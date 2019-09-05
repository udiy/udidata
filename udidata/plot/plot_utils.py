from .. import utils

#######################################################################################################################

def scatter_geo(ds, prop="pressure", stat="count"):
    """
    Takes in xarray Dataset and creates a tidy and clean pandas DataFrame for plotting with plotly
    
    Parameters
    ----------
    ds : xarray Dataset
        A dataset of aggregated data with a specified format

    prop : str, default 'pressure'
        Atmospheric property of interest
        
    stat : str, default 'count'
        A statistic of interest to show on the plot. Options: count, mean, median, std, min, max
    
    Returns
    -------
    df : pandas DataFrame
        A 'tidy' dataframe suitable for plotting data
    """
    
    if stat.lower()=="total count":
        stat = "count"
        da = ds.sel(stat=stat)[prop]
        da = da.sum(dim="date")
    else:
        da = ds.sel(stat=stat)[prop]
        
    # transform data to pandas DataFrame so it's easier to plot with plotly. And clean dataframe
    df = da.to_dataframe(name=stat)
    df = df.dropna().drop(["stat"], axis=1)
    df = df[df[stat]>0]
    if (df[stat].max() - df[stat].min()) > 100:    # if values range is bigger than 2 orders of magnitude then scale column
        df = df.scale_column(col=stat)
    df = df.reset_index()
    
    return df

#######################################################################################################################

def lines(ds, prop="pressure", stat="mean"):
    """
    Takes in xarray Dataset and creates a pandas DataFrame suitable for line chart, with x axis as date dimension.

    Parameters
    ----------
    ds : xarray Dataset
        A dataset of aggregated data with a specified format

    prop : str, default 'pressure'
        Atmospheric property of interest
        
    stat : str, default 'count'
        A statistic of interest to show on the plot. Options: count, mean, median, std, min, max
    
    Returns
    -------
    df : pandas DataFrame
        A 'tidy' dataframe suitable for plotting data
    """

    da = ds.sel(stat=stat)[prop]
    df = da.to_dataframe(name=stat).drop(["stat"], axis=1)
    
    df = df.dropna().reset_index()
    df = df.zip_columns(["lat","lng"])
    
    return df