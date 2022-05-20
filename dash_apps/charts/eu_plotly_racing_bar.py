"""
Questions addressed:
What are the rankings of EU countries in yearly greenhouse emission from 2010 to 2017?

Author: Yuansheng Zhang (18019413)

Reason for the chart type:
Racing bar chart

Library used: sqlite3, Plotly.graph_objects, pandas, random

Refernece
A part of code below is adapted from Towards_Data_Science blog. Arthur:Luis Chaves.
[Source Code]: https://towardsdatascience.com/making-a-bar-chart-race-plot-using-plotly-made-easy-8dad3b1da955
"""
import sqlite3
import pandas as pd
from random import sample
import plotly.graph_objects as go
import pathlib


def eu_plotly_racing_bar_chart ():

    con = sqlite3.connect( 'data/Updated_EuroStat.db' )
    cur = con.cursor()
    print( pathlib.Path().absolute() )


    # get country list and remove country with null data
    cur.execute( "SELECT name FROM sqlite_master" )
    country_names = cur.fetchall()
    for i in range( len( country_names ) ):
        country_names[i] = str( country_names[i][0] )
    country_names.remove( "EU_27_countries" )
    country_names.remove( "Serbia" )
    country_names.remove( "Ireland" )


    # get year list
    cur.execute( "SELECT time FROM EU_27_countries" )
    years = cur.fetchall()

    # get data list
    gases = list()
    for name in country_names:
        cur.execute( "SELECT Greenhouse_gases FROM {0}".format( name ) )
        gases.append( cur.fetchall() )

    # transform country list elements into string
    for i in range( len( years ) ):
        years[i] = str( years[i][0] )

    # transform table elements into number
    for i in range( len( country_names ) ):
        for j in range( len( years ) ):
            gases[i][j] = float( gases[i][j][0] )

    # Create dataframe
    df = pd.DataFrame( gases )
    df.columns = years
    df['Country'] = country_names

    # Code below is adapted from Towards_Data_Science blog. Arthur:Luis Chaves.
    # [Source Code]: https://towardsdatascience.com/making-a-bar-chart-race-plot-using-plotly-made-easy-8dad3b1da955

    # map colours to countries
    colours = ['rgb({}, {}, {})'.format( *sample( range( 256 ), 3 ) ) for country in country_names]
    df['Colour'] = colours

    # create default frame
    frame1 = df[['Country', '2010', 'Colour']]
    frame1 = frame1.sort_values( '2010', ascending=True )

    # define data and layout of the default frame
    fig = {"frames": [], 'data': go.Bar(
        x=frame1['2010'],
        y=frame1['Country'],
        marker_color=frame1['Colour'],
        hoverinfo='x+y',
        textposition='outside',
        texttemplate='%{y}: %{x:.4s}',
        orientation='h'
    ),
        'layout': go.Layout(
        font={'size': 13},
        plot_bgcolor='white',
        xaxis={'showline': True,
               'visible': True,
               'range': (0, frame1['2010'].max() + 20),
               'title_text': 'Annual Green House Gas Emission (CO2 Equivalent)'
               },
        yaxis={'showline': False,
               'visible': True,  # to show the title
               'showticklabels': False,  # to avoid displaying the names
               'title_text': 'Countries'},
        bargap=0.3,
        title='Rankings of EU countries in Annual Greenhouse Gas Emission from 2010 to 2017'
    )}

    # add buttons
    fig["layout"]["updatemenus"] = [
        {
            "buttons": [  # define our buttons: Play and Pause
                {
                    "args": [None, {"frame": {"duration": 1000  # how long the frame is still (in milliseconds)
                        , "redraw": False},  # for optimised rendering
                                    "fromcurrent": True,
                                    "transition": {"duration": 500,  # duration of the transition btwn frames
                                                   "easing": "quadratic-in-out"}}],
                    "label": "Play",  # label to be displayed
                    "method": "animate"  # other options are relayout, restyle and update.
                },
                {
                    "args": [[None], {"frame": {"duration": 0,
                                                "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            # for left-to-right appearance,
            # change to 'up' for top-to-bottom appearance
            "direction": "left",
            # right and top padding
            "pad": {"r": 10, "t": 87},
            # whether to display button in shaded color when pressed
            "showactive": True,
            "type": "buttons",  # specify we are using buttons and not dropdown
            # position in figure (relative)
            "x": 0.1,
            "y": 0
        }
    ]

    # add slider
    sliders_dict = {
        "active": 0,
        "yanchor": "top",
        "xanchor": "left",
        "currentvalue": {
            "font": {"size": 20},
            "prefix": "Year:",
            "visible": True,
            "xanchor": "right"
        },
        "transition": {"duration": 1000, "easing": "cubic-in-out"},
        "pad": {"b": 10, "t": 50},
        "len": 0.9,
        "x": 0.1,
        "y": 0,
        "steps": []
    }

    # define animated frames similarly to frame 1
    for year in range( int( min( years ) ), int( max( years ) ) + 1 ):
        # 1 Same steps than what what we did with frame1
        snap_data = df[['{0}'.format( year ), 'Country', 'Colour']]
        snap_data = snap_data.sort_values( '{0}'.format( year ), ascending=True )

        # 2 make frame
        frame = go.Frame(
            data=[
                go.Bar(
                    x=snap_data['{0}'.format( year )],
                    y=snap_data['Country'],
                    marker_color=snap_data['Colour'],
                    hoverinfo='x+y',
                    textposition='outside',
                    texttemplate='%{y}: %{x:.4s}',
                    orientation='h'
                )
            ],
            layout=go.Layout(
                font={'size': 13},
                plot_bgcolor='white',
                xaxis={'showline': True,
                       'visible': True,
                       'range': (0, df['{0}'.format( year )].max() + 20)
                       },
                yaxis={'showline': False,
                       'visible': False
                       },
                bargap=0.3,
                title='Rankings of EU countries in Annual Greenhouse Gas Emission from 2010 to 2017'
            ),
            name=year
        )

        fig['frames'].append( frame )

        # 3 Define slider step so that is linked to the latest frame
        slider_step = {"args": [
            [year],  # this one needs to match the frame name
            {"frame": {"duration": 1000, "redraw": False},
             "mode": "immediate",
             "transition": {"duration": 1000}}
        ],
            "label": year,  # This one defines the sliders tick names
            "method": "animate"}  # same as with buttons
        ##.2 Append to sliders_dict
        sliders_dict["steps"].append( slider_step )

        # 4 Modify layout sliders of our figure
        fig['layout']['sliders'] = [sliders_dict]

    return go.Figure( fig )
