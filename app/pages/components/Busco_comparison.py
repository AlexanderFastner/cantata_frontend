# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from pages.components.heatmap import get_species_list
#----------------------------------------------------------

dash.register_page(__name__, path="/Busco")

layout = html.Div(
    [
        html.Div(
            [
                dbc.Card(
                    [
                        dbc.CardHeader(html.H5("Select species for comparison")),
                        dbc.CardBody(
                            [
                                #call function to get species names
                                #add selection option for main groups/all
                                #Also radio buttons for each species
                                dcc.Checklist(
                                    options=get_species_list()
                                ),
                                #generate heatmap based on the selected input
                            ],
                        )
                    ],
                    style={'width': '20%', 'height': '100%'},
                ),
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Label("Downloads: download this heatmap as .png"),
                            #TODO
                        ],
                    )
                ),
            ],
        ),
        dcc.Location(id="url", refresh=False),
    ]
)