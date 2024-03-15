# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
import dash_bootstrap_components as dbc
from pages.components.user_selection import get_species_list, group_options
from pages.components.tabs import plot_selector_tabs
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
#----------------------------------------------------------
dash.register_page(__name__, path="/Busco")
#----------------------------------------------------------

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
                                            id="group_dropdown",
                                            options=[{'label': category['label'], 'value': category['value']} for category in group_options],
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


@callback(
    Output('species_selected', 'values'),
    Input('group_dropdown', 'value')
)
def update_checklist_options(selected_value):
    print(selected_value)
    updated_options = get_updated_species_list(selected_value)
    return updated_options

def get_updated_species_list(selected_value):
    # Implement your logic here to generate updated species list based on selected value
    # Return a list of dictionaries with 'label' and 'value' keys for each option
    pass