#main page containing info and various tools
#----------------------------------------------------------
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
#----------------------------------------------------------
dash.register_page(__name__, path="/")
#----------------------------------------------------------
layout = html.Div([
    #TODO restrict this to the left side of the screen
    #TODO add logo
    #TODO add styling and background colors
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Markdown('''
                    # About: \n
                    add some text explain the purpose of website\n
                    link to future paper
                    '''),
                ],
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    #TODO add url navigation to go straight to the appropriate tab
                    dcc.Markdown('''
                    ## Tools we offer: \n             
                    ### [Heatmap of buscos](/Busco)\n
                    ### [Stacked Area plots](/Busco)\n
                    ### [Raincloud plots](/Busco)\n
                    ### [Alignment Comparison](/Busco)\n
                    ...future tools\n
                    '''),

                    html.Hr(),
                    dcc.Markdown('''
                    # Our Data: \n             
                    where our data is from\n
                    Brief overview of available species\n
                    Add Overview Tree Here!
                    link to figshare\n
                    '''),
                ],
            )
        ),
    ],
    style={"width": "60%", 'display': 'inline-block'},
)