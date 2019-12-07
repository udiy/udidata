import numpy as np
import plotly.graph_objects as go
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

#######################################################################################################################

def add_dropdown(figure):

    """
    In case of a figure with multiple traces, adds dropdown menu to the figure.
    """

    num_traces = len(figure.data)
    
    if num_traces > 1:
        
        buttons = [dict(label=i+1, 
                method="update", 
                args=[dict(visible=np.insert(np.zeros(num_traces-1, dtype=bool), i, 1)), 
                      dict(title=figure.data[i].name)])
                   for i in range(num_traces)]
        
        figure.update_layout(updatemenus=[go.layout.Updatemenu(active=0, buttons=buttons)], 
                             title_text=figure.data[0].name)
        
        # make only the first trace visible, at first
        figure.data[0].visible = True

        for i in range(1,num_traces):
            figure.data[i].visible = False

#######################################################################################################################

def scatter_geo_layout(figure, deg=2.5):
    
    """
    Defines a template for displaying scatter geo plots

    Parameters
    ----------
    figure: plotly.graph_objs._figure.Figure
        Plotly figure geo object i.d. scatter_geo
        
    deg: float, default 2.5
        Degrees for grid spacing
        
    Returns
    -------
    figure: plotly.graph_objs._figure.Figure
        Better layout figure
    """

    grid_dict = dict(showgrid = True,
                     gridcolor = "black",
                     gridwidth=0.1,
                     dtick=deg)

    geo_dict = dict(projection_type='natural earth',
                    showcountries=True, 
                    countrycolor="white",
                    showcoastlines=False,
                    showland=True,
                    landcolor="#c2c2c2",
                    showocean=True,
                    oceancolor="#e6fcfc",
                    showlakes=True,
                    lakecolor="#3399FF",
                    showrivers=True,
                    showframe=False,
    #                 bgcolor="#f2eded",
                    lonaxis=grid_dict,
                    lataxis=grid_dict)

    colorbar_dict = dict(thicknessmode="fraction",
                         thickness=0.01,
                         xpad=0)


    figure.update_layout(coloraxis={"colorbar": colorbar_dict, "colorscale": "jet"},
                      margin={"l":0, "b":0, "t":50},
                      geo=geo_dict)

#######################################################################################################################