# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from pages.components.user_selection import get_species_list
from pages.components.tabs import plot_selector_tabs
#----------------------------------------------------------

dash.register_page(__name__, path="/Busco")

layout = html.Div(
    [
        dbc.Row( #top level row
            [
                dbc.Col( #left column for selection
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5("Select species for comparison")),
                                dbc.CardBody(
                                    [
                                        dcc.Dropdown(
                                            options=[
                                                {"label": "All", "value": "All"},
                                                #TODO SERGIO
                                                {"label": "Cnideria", "value": "SERGIO please add a list of cniderians here!"},
                                                {"label": "None", "value": "None"},
                                            ],
                                            placeholder="Select a Group",
                                        ),
                                        html.Hr(),
                                        dcc.Checklist(
                                            id='species_selected',
                                            options=get_species_list(),
                                            value=[]
                                        ),                           
                                    ],
                                ),
                            ],
                            style={"width": "100%", 'display': 'inline-block'},
                        ),
                    width="auto",
                ),

                dbc.Col( # middle/right column for plotting
                    
                    #tabs for the various possible plots
                    [
                        plot_selector_tabs
                    ],
                    style={"width": "80%", 'display': 'inline-block'},
                ),
            ],
        ),

    ],
    style={"width": "100%", 'display': 'inline-block'}
)