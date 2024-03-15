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
                    dcc.Markdown('''
                    # Tools we offer: \n             
                    #what tools analysis are there\n
                    #heatmap of buscos\n
                    #raincloud plots?\n
                    #...\n
                    #future tools\n
                        #make trees\n
                        #other ways to compare or inspect selected data\n
                    '''),

                    html.Hr(),
                    dcc.Markdown('''
                    # Our Data: \n             
                    where our data is from\n
                    brief overview of available species\n
                    link to figshare?\n
                    '''),
                ],
            )
        ),
    ],
    style={"width": "60%", 'display': 'inline-block'},
)