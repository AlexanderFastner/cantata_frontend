#main page containing info and various tools
#----------------------------------------------------------
import collections
import dash
import dash_bootstrap_components as dbc
from dash import html
#----------------------------------------------------------
dash.register_page(__name__, path="/")


layout = html.Div([
    #TODO restrict this to the left side of the screen
        dbc.Card(
            dbc.CardBody(
                [
                    html.Label("About:"),
                    #add some text explain the purpose of website
                    #link to future paper
                ],
            )
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    html.Label("Tools we offer: "),
                    #what tools analysis are there
                    #heatmap of buscos
                    #raincloud plots?
                    #...
                    #future tools
                        #make trees
                        #other ways to compare or inspect selected data
                    html.Hr(),
                    html.Label("Our Data: "),
                    #where our data is from
                    #brief overview of available species
                    #link to figshare?
                ],
            )
        ),
    ]
)
#----------------------------------------------------------





#----------------------------------------------------------

