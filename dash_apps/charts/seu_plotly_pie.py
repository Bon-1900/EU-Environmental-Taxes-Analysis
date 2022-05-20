'''Contributers: Yuansheng Zhang'''

import plotly.express as px
import pandas as pd
from dash_apps.sqlite import SQLite

def seu_plotly_pie ():
    # Get data
    database = SQLite( 'data/Updated_EuroStat.db' )
    country_list = ['Greece', 'Italy', 'Malta', 'Portugal', 'Serbia', 'Slovenia', 'Spain']
    data = database.get_data_for_countries(
        countries=country_list )
    df = pd.DataFrame( data, columns=['country', 'year', 'investments'] )
    df = df[df.year >= 2014]

    # create the pie char for total investments
    investment_total = []
    for country in country_list:
        investment_total.append( sum( df[df.country == country].investments.tolist() ) )
    fig_total = px.pie( values=investment_total, names=country_list )

    return fig_total

