'''Contributers:Tasha Tahir, Yuansheng Zhang'''

import pandas as pd
import plotly.express as px
from dash_apps.sqlite import SQLite

def seu_plotly_dot():

    database = SQLite('data/Updated_EuroStat.db')

    df = pd.DataFrame(database.get_data_for_countries(countries=[
        'Greece', 'Italy', 'Malta', 'Portugal', 'Slovenia', 'Spain'
    ]))

    figure = px.scatter(
        data_frame=df,
        title='Air Pollutants VS Environmental Taxes Paid by South EU Countries Over Time',
        y='pollution',
        x='tax',
        hover_name='country',
        animation_frame='year',
        color='country',
    )

    figure.update_layout(
        xaxis=dict(
            title='Environmental Taxes',
        ),
        yaxis=dict(
            title='Air Pollutants',
        )
    )

    figure.update_traces(marker=dict(size=25))
    figure.update_xaxes(nticks=50)
    return figure
