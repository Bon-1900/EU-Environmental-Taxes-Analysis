'''Contributers:Isabella Dube-Miglioli, Yuansheng Zhang'''

import pandas as pd
import plotly.express as px
from dash_apps.sqlite import SQLite

def italy_plotly_sunburst():

    # Create lists to store the data, specifying all indicators and years, and extract the data for Italy from the
    # database into the corresponding lists.
    database = SQLite('data/Updated_EuroStat.db')
    data = database.get_data_for_countries(countries=['Italy'])

    Years = 4*[row.get('year') for row in data]
    Air_pollutants = [row.get('pollution') for row in data]
    Environmental_taxes = [row.get('tax') for row in data]
    Greenhouse_gases = [row.get('gases') for row in data]
    Investments = [row.get('investments') for row in data]

    # Create lists storing the data, the total and the name of all indicators, and empty lists to store the normalised
    # data and the hover-text.
    Lists_of_values = [Air_pollutants, Environmental_taxes, Greenhouse_gases, Investments]
    Sums = [sum(Air_pollutants), sum(Environmental_taxes), sum(Greenhouse_gases), sum(Investments)]
    Indicators = sorted(8*['Air pollutants', 'Environmental taxes', 'Greenhouse gases', 'Investments'])
    Normalised_data = []
    Hover_tags = []

    # Declare a 'Counter' for iteration, and use a for-loop and if-else loops to calculate and store the normalised data
    # into its corresponding list, specifying the appropriate units for each value calculated depending on the indicator.
    Counter = 0
    for indicator_group in Lists_of_values :
        for value in indicator_group :
            if Counter < 8 :
                Normalised_data.append(round((25 * value / Sums[0]), 2))
                Hover_tags.append(str(value) + ' Particulates < 10 µm')
            else :
                if Counter < 16 :
                    Normalised_data.append(round((25 * value / Sums[1]), 2))
                    Hover_tags.append(str(value) + ' millions of euros')
                else :
                    if Counter < 24 :
                        Normalised_data.append(round((25 * value / Sums[2]), 2))
                        Hover_tags.append(str(value) + ' tons of CO2 equivalent')
                    else :
                        Normalised_data.append(round((25 * value / Sums[3]), 2))
                        Hover_tags.append(str(value) + ' millions of euros')
            Counter += 1

    # Create the dataframe from a dictionary of arrays corresponding to each parameter.
    data_dictionary = {'Years' : Years,
                       'Indicators' : Indicators,
                       'Percentages' : Normalised_data,
                       'Labels' : Hover_tags}

    df = pd.DataFrame(data = data_dictionary)

    # Create the figure and update the layout and traces.
    Italy_sunburst =px.sunburst(
        df,
        path = ['Indicators','Years'],
        values = 'Percentages',
        hover_name = None,
        hover_data= {'Indicators':False},
        custom_data = ['Labels'],
        width = 800,
        height = 800,
        color = 'Indicators',
        color_discrete_map={'Air pollutants':'#ccffcc', 'Environmental taxes':'#b3fff0', 'Greenhouse gases':'#99ffcc',
                            'Investments':'#99ffff'},)

    Italy_sunburst.update_layout(
        title = {'text' : "<b> Evolution of all indicators in Italy from 2010 to 2017</b>", 'x':0.5, 'xanchor':'center'},
        font_family="Open Sans",
        font_color="#0f3d3d",
        font_size=12.5,
        title_font_family="Open Sans",
        title_font_color="#00394d",
        title_font_size=25,)

    Italy_sunburst.update_traces(
        hovertemplate = '%{customdata[0]}',)

    return Italy_sunburst
