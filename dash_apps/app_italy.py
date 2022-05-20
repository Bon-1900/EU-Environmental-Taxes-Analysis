'''Contributers: Yuansheng Zhang'''

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash import Dash
from dash.dependencies import Input, Output

from dash_apps.charts.italy_plotly_sunburst import italy_plotly_sunburst


class DashAppItaly:
    def __init__( self, flask_server ):
        self.app = Dash( name=self.__class__.__name__,
                         routes_pathname_prefix='/dash_app_italy/',
                         suppress_callback_exceptions=True,
                         server=flask_server,
                         external_stylesheets=[dbc.themes.LUX],
                         meta_tags=[{
                             'name': 'viewport',
                             'content': 'width=device-width, initial-scale=1.0'
                         }])
        self._fig1 = italy_plotly_sunburst()

    def setup( self ):
        self.setup_layout()

    def setup_layout( self ):
        self.app.layout = dbc.Container( fluid=True, children=[
            dbc.NavbarSimple(
                children=[
                    dbc.NavItem( dbc.NavLink( "Home", href="/", external_link=True ) ),
                    dbc.DropdownMenu( [dbc.DropdownMenuItem(
                                           dbc.NavLink( "EU", href="/dash_app_eu", external_link=True,
                                                        style={"color": "black"} ) ),
                                        dbc.DropdownMenuItem(
                                            dbc.NavLink( "Southern EU", href="/dash_app_s_eu", external_link=True,
                                                         style={"color": "black"} ) ),
                                       dbc.DropdownMenuItem(
                                           dbc.NavLink( "Spain", href="/spain_img", external_link=True,
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
            html.H2( 'Italy' ),
            html.Br(),
            dcc.Graph( figure=self._fig1 )
        ] )

