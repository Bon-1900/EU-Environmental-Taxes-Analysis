'''Contributers: Yuansheng Zhang'''

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output

from dash_apps.charts.seu_plotly_pie import seu_plotly_pie
from dash_apps.charts.seu_plotly_dot import seu_plotly_dot


class DashAppSEU:
    def __init__( self, flask_server ):
        self.app = Dash( name=self.__class__.__name__,
                         routes_pathname_prefix='/dash_app_s_eu/',
                         suppress_callback_exceptions=True,
                         server=flask_server,
                         external_stylesheets=[dbc.themes.LUX],
                         meta_tags=[{
                             'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'
                         }]
                         )
        self.question_list = []
        self.question_list.append(
            'Air Pollutants VS Environmental Taxes Paid by South EU Countries Over Time' )
        self.question_list.append(
            'Total Investment in Southern EU in the Period of 2014~2017' )

        self._fig2 = seu_plotly_pie()
        self._fig1 = seu_plotly_dot()

    def setup( self ):
        self.setup_layout()
        self.setup_callbacks()

    def setup_layout( self ):
        self.app.layout = dbc.Container( fluid=True, children=[
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem( dbc.NavLink( "Home", href="/", external_link=True ) ),
                    dbc.DropdownMenu( [dbc.DropdownMenuItem(
                                            dbc.NavLink( "EU", href="/dash_app_eu/", external_link=True,
                                                         style={"color": "black"} ) ),
                                       dbc.DropdownMenuItem(
                                           dbc.NavLink( "Italy", href="/dash_app_italy/", external_link=True,
                                                        style={"color": "black"} ) ),
                                       dbc.DropdownMenuItem(
                                           dbc.NavLink( "Spain", href="/spain_img/", external_link=True,
                                                        style={"color": "black"} ) )],
                                      label="Interactivity",
                                      nav=True ),
                    dbc.NavItem( dbc.NavLink( "Community", href="/community/blog", external_link=True ) ),
                    dbc.NavItem( dbc.NavLink( "Logout", href="/signup/logout", external_link=True ) )
                ],
                brand="Group 3",
                brand_href="#",
                color="primary",
                dark=True,
            ),
            html.Br(),
            html.H2( 'Southern EU Region' ),
            html.Br(),
            html.H4( "Select Chart" ),
            dcc.Dropdown( id="question_select",
                          options=[{"label": x, "value": x} for x in self.question_list],
                          value=self.question_list[0] ),
            dcc.Graph( id='chart' )
        ] )

    def setup_callbacks( self ):
        @self.app.callback( Output( "chart", "figure" ), [Input( "question_select", "value" )] )
        def update_recycling_chart( question ):
            if question == self.question_list[0]:
                fig = self._fig1
            elif question == self.question_list[1]:
                fig = self._fig2
            return fig
