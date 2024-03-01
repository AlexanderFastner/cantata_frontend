# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from pages.components.heatmap import get_species_list, heatmap
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
                                            options=get_species_list()
                                        ),                           
                                    ],
                                ),
                            ],
                            style={"width": "100%", 'display': 'inline-block'},
                        ),
                    width="auto",
                ),

                dbc.Col( # middle/right column for heatmap
                    [
                        html.Div(heatmap, id="heatmap"),
                        dcc.Location(id="url", refresh=False),

                        html.Div( #add download option
                            [
                                dbc.Row(
                                    dbc.Col(
                                        dbc.Card(
                                            [
                                                dbc.CardBody(
                                                    [
                                                        dbc.Button('Download this Heatmap', id='download-heatmap-button')
                                                    ],
                                                )
                                            ],
                                        ),
                                        #style={"width": "20%", "align": "end"},
                                    ),
                                    style={"width": "15%"}
                                ),
                            ],
                        ),

                    ],
                    style={"width": "80%", 'display': 'inline-block'},
                ),
            ],
        ),

    ],
    style={"width": "100%", 'display': 'inline-block'}
)