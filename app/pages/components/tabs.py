# Organize the various tabs
#----------------------------------------------------------
import dash_bootstrap_components as dbc
from dash import dcc, html
#----------------------------------------------------------
#TODO for each tab add download buttons

#----------------------------------------------------------
#TEST
from dash import dcc, callback
from dash.dependencies import Input, Output, State
@callback(
    Output('output', 'children'),
    Input('species_selected', 'value')
)
def print_species_value(species_selected):
    print("Selected species:", species_selected)
    return ""

tab_heatmap = html.Div(
    [
        dbc.Row(html.H1("Species v. Buscos Heatmap")),

        #TODO add selectors to switch between the Protein buscos and the transpi/trinity ones
        #TODO add selector for difference heatmap
        #TODO dif heatmp is the difference calculated betweeen the different heatmaps to more easily spot differences
            #TODO selector of what to calculate differencces between (protein/transpi, protein/trinity, trinity/transpi)

        dcc.Graph(id='busco_heatmap'),
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_stacked_area= html.Div(
    [
        dbc.Row(html.H1("Stacked Area Plots of TransPi and Trinity Buscos")),

        #stacked area plots for Transpi/Trinity
        dcc.Graph(id='TransPi_area'),
        dcc.Graph(id='Trinity_area'),
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_raincloud= html.Div(
    [
        dbc.Row(html.H1("Raincloud Plots")),
        #dcc.Graph(id='my_stacked_barplot'),
    ],
    className="mt-3",
)
#----------------------------------------------------------
plot_selector_tabs = html.Div(
    [
        dbc.Tabs(
            id="tabs",
            active_tab="tab_active",
            children=[
                dbc.Tab(tab_heatmap, label="Heatmap", tab_id="tab_heatmap"),
                dbc.Tab(tab_stacked_area, label="Stacked Area", tab_id="tab_stacked_area"),
                dbc.Tab(tab_raincloud, label="Raincloud Plot", tab_id="tab_raincloud"),
            ],
        ),
        html.Div(id="tab-content", style={"marginBottom": "10px"}),
    ]
)
#----------------------------------------------------------

