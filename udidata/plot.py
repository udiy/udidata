import numpy as np
import plotly.express as px

#######################################################################################################################

def tidy_df(ds, stat="count"):
    """
    Takes in xarray Dataset and creates a tidy and clean pandas DataFrame for plotting with plotly
    
    Parameters
    ----------
    ds : xarray Dataset
        A dataset of aggregated data with a specified format
        
    stat : str, default 'count'
        A statistic of interest to show on the plot. Options: count, mean, median, std, min, max
    
    Returns
    -------
    df : pandas DataFrame
        A 'tidy' dataframe suitable for plotting data
    """
    if stat.lower()=="sum":
        stat = "count"
        da = ds.sel(stat=stat)["pressure"]
        da = da.sum(dim="date")
    else:
        da = ds.sel(stat=stat)["pressure"]
        
    
    # transform data to pandas DataFrame so it's easier to plot with plotly. And clean dataframe
    df = da.to_dataframe(name=stat)
    df = df.dropna()
    df = df.drop(["stat"], axis=1)
    df = df[df[stat]>0]
    df[f"scaled_{stat}"] = np.log10(df[stat])    # create a new column with logarithminc scale for stat
    df = df.reset_index()
    
    return df

#######################################################################################################################

def scatter_geo(ds, stat="count", title=None, cmap="ylorrd"):
    """
    Plot a scatter plot on top of a world map baesd on df.
    
    Parameters
    ----------
    df : pandas DataFrame
        A 'tidy' clean dataframe suitable for plotting with plotly
        
    stat : 
    
    Returns
    -------
    None
    """ 
    df = tidy_df(ds, stat)
    
    if stat=="sum":
        stat = "count"
        animation_frame = None
    else:
        animation_frame = "date"

    scaled_stat_col = f"scaled_{stat}"    # column name of scaled variable in df
    fig = px.scatter_geo(df, lat="lat", lon="lng", size=scaled_stat_col, color=scaled_stat_col, 
                         hover_data=[stat], title=title, animation_frame=animation_frame, 
                         projection="natural earth", color_continuous_scale=cmap)
    fig.show()