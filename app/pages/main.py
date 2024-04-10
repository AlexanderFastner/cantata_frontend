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
                    ## Analyze Buscos: \n             
                    ### [Heatmap of buscos](/Busco)\n
                    ### [Stacked Area plots](/Busco)\n
                    ### [Raincloud plots](/Busco)\n
                    ### [Alignment Comparison](/Busco)\n
                    ...future tools\n
                    '''),
                    #This is to showcase what the user can do
                    #TODO arrange and resize these
                    html.Img(src=dash.get_asset_url("heatmap_example.png"), height="600px"),
                    html.Img(src=dash.get_asset_url("stacked_area_example.png"), height="600px"),
                    html.Img(src=dash.get_asset_url("raincloud_example.png"), height="600px"),
                    html.Img(src=dash.get_asset_url("log_diff_example.png"), height="600px"),
                    html.Img(src=dash.get_asset_url("alignment_example.png"), height="600px"),

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