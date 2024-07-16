#This page contains a link to various tutorials for usinng Cantata
#----------------------------------------------------------
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
#----------------------------------------------------------
dash.register_page(__name__, path="/Tutorials")
#----------------------------------------------------------
layout = html.Div(
    [
        #Tutorial 1
        dbc.Row(
            [
                dbc.Col(
                    [  
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5("Tutorial for ______")),
                                dbc.CardBody(
                                    [
                                        dcc.Markdown(
                                            """
                                            ## Tutorial Content 1
                                            ...
                                            ...
                                            ### Step 2
                                            ...
                                            ...
                                            """
                                        ),
                                    ],
                                )
                            ]
                        ),
                        #Tutorial 2
                        dbc.Row(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H5("Tutorial for Something else")),
                                        dbc.CardBody(
                                            [
                                                dcc.Markdown(
                                                    """
                                                    ## Tutorial Content 2
                                                    ...
                                                    ...
                                                    ### Step 2
                                                    ...
                                                    ...
                                                    """
                                                ),
                                            ],
                                        )
                                    ]
                                )
                            ]
                        ),
                    ],width={"size": "12", "offset": "0"},
                )
            ]
        )
    ]
)
#----------------------------------------------------------