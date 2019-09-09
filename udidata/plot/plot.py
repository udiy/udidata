import plotly.express as px
from . import plot_utils

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

    df = plot_utils.scatter_geo(ds, prop, stat)
    
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

#######################################################################################################################

def lines(ds, prop="pressure", stat="mean", title=None):
    """
    Plot trend lines across date dimension

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

    df = plot_utils.lines(ds, prop, stat)
    num_of_colors = len(df["latlng"].drop_duplicates())
    print(f"Number of lines: {num_of_colors}")
    print("""\nIn the legend:
    - Double click on a specific line to hide all the rest of the lines
    - Single click on a line to hide it""")
    fig = px.line(df, x="date", y=stat, color="latlng", title=title)
    
    return fig
