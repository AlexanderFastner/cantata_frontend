# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
#----------------------------------------------------------

dash.register_page(__name__, path="/Busco")

layout = html.Div(
    [
        html.Div(
            [
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.Label("Data: select species for comparison"),
                            #add selection option (radio buttons?, select all button?)

                        ],
                    )
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