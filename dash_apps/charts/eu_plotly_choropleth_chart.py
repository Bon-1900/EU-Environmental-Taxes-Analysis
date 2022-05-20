'''Contributers: Isabella Dube-Miglioli, Yuansheng Zhang'''

import plotly.express as px
import pandas as pd
from dash_apps.sqlite import SQLite

def eu_plotly_choropleth_chart ():
    # Create lists to store the data, specifying country names, environmental taxes and years, and extract the data from the
    # database into the corresponding lists for all EU-members.
    Database = SQLite( 'data/Updated_EuroStat.db' )

    Data = Database.get_data_for_countries(countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czechia',
           'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia',
           'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia',
           'Spain', 'Sweden', 'United_Kingdom'])

    Environmental_taxes = [row.get('tax') for row in Data]
    Country_names = [row.get('country') for row in Data]
    Years = [row.get('year') for row in Data]

    # Create a counter and a list specifying the ISO codes for all EU-members, and use iteration through a for-loop to
    # create an array of ISO-codes to be used in the dataframe.
    ISO_codes = ['AUT','BEL','BGR','HRV','CYP','CZE','DNK','EST','FIN','FRA','DEU','GRC','HUN','IRL','ITA','LVA',
                 'LTU','LUX','MLT','NLD','POL','PRT','ROU','SVK','SVN','ESP','SWE','GBR']
    ISO_codes_list = []
    Counter = 0

    for ISO_code in ISO_codes :
        while Counter < 8 :
            ISO_codes_list.append(ISO_code)
            Counter += 1
        Counter = 0

    # Create the dataframe from a dictionary of arrays corresponding to each parameter.
    data_dictionary = {'Year ' : Years,
                       'Country code ' : ISO_codes_list,
                       'Environmental taxes (millions of €) ' : Environmental_taxes,
                       'Label ' : Country_names}

    df = pd.DataFrame(data = data_dictionary)

    # Create the figure and update the layout to change the fonts and titles.
    EU_map = px.choropleth(df,
                            locations = 'Country code ',
                            color = 'Environmental taxes (millions of €) ',
                            hover_name ='Label ',
                            hover_data = {'Country code ':None},
                            custom_data = ['Label ','Environmental taxes (millions of €) '],
                            animation_frame = 'Year ',
                            animation_group = 'Environmental taxes (millions of €) ',
                            fitbounds = 'locations',
                            width = 1300,
                            color_continuous_scale = px.colors.sequential.Teal,
                            color_continuous_midpoint= 25000)

    EU_map.update_layout(
        title = {'text' : "<b> Environmental taxes in the EU from 2010 to 2017</b>", 'x':0.5, 'xanchor':'center'},
        legend_title_text ="Environmental taxes (millions of euros)",
        legend_title_font_color="green",
        font_family="Open Sans",
        font_color="black",
        font_size=12.5,
        title_font_family="Open Sans",
        title_font_color="#00394d",
        title_font_size=25,)

    return EU_map

