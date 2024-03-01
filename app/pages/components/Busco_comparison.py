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
        dbc.Row(
            [
                html.Div(
                    [
                        dbc.Col(
                            [
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
                                                    options=get_species_list()
                                                ),                           
                                            ],
                                        )
                                    ],
                                ),
                                dbc.Card(
                                    [
                                        dbc.CardBody(
                                            [
                                                html.Label("Download this heatmap as .png"),
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                    style={'width': '20%', 'display': 'inline-block'}
                ),
                dbc.Col(
                    [
                        html.Div(heatmap),
                        dcc.Location(id="url", refresh=False),
                    ],
                    style={'width': '80%', 'display': 'inline-block'},
                )
            ]
        )
    ]
)