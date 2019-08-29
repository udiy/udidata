import numpy as np
import plotly.express as px
from . import utils, transform

#######################################################################################################################

def scatter_geo(ds, prop="pressure", stat="count", title=None, cmap="ylorrd"):
    """
    Plot a scatter plot on top of a world map baesd on df.
    
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
    fig : plotly.graph_objs._figure.Figure
        Plotly figure
    """ 
    df = transform.tidy_df(ds, prop, stat)
    
    if stat=="total count":
        stat = "count"
        animation_frame = None
    else:
        animation_frame = "date"

    scaled_col = f"scaled_{stat}"    # column name of scaled variable in df
    size_col = scaled_col if scaled_col in df.columns else stat    # determine which column shapes size and color
    
    fig = px.scatter_geo(df, lat="lat", lon="lng", size=size_col, color=size_col, 
                         hover_data=[stat], title=title, animation_frame=animation_frame, 
                         projection="natural earth", color_continuous_scale=cmap)

    return fig