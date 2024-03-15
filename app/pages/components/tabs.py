# Organize the various tabs
#----------------------------------------------------------
import dash_bootstrap_components as dbc
from dash import dcc, html
from pages.components.user_selection import get_busco_genes, get_busco_functions
#----------------------------------------------------------
#TODO for each tab add download buttons
#----------------------------------------------------------
tab_heatmap = html.Div(
    [
        dbc.Row(html.H1("Species v. Buscos Heatmap")),
        #selector to switch between the Protein buscos and the transpi/trinity ones
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="heatmap_selector",
                        options=[
                            "Protein","TransPi","Trinity"
                        ],
                        multi=True,
                        placeholder="Select transciptome",
                    ),
                ],
            ),
        ),
        dcc.Graph(id='busco_heatmap'),
        html.Hr(),
        #TODO dcc.Graph(id='busco_difference_heatmap'),
        html.Button('Download Heatmap', id='download-heatmap'),
        html.Button('Download Difference Heatmap', id='download-difference-heatmap', n_clicks=0),
        #TODO dif heatmp is the difference calculated betweeen the different heatmaps to more easily spot differences
            #TODO selector of what to calculate differencces between (protein/transpi, protein/trinity, trinity/transpi)
        #dcc.Graph(id='difference_heatmap'),
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_stacked_area= html.Div(
    [
        dbc.Row(html.H1("Stacked Area Plots of TransPi and Trinity Buscos")),
        #stacked area plots for Transpi/Trinity
        dcc.Graph(id='TransPi_area'),
        html.Hr(),
        dcc.Graph(id='Trinity_area'),
        html.Button('Download Stacked Area TransPi', id='download-stacked-area-TransPi', n_clicks=0),
        html.Button('Download Stacked Area Trinity', id='download-stacked-area-Trinity', n_clicks=0),
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_raincloud= html.Div(
    [
        dbc.Row(html.H1("TransPi v. Trinity Raincloud Plots")),
        dcc.Graph(id='TransPi_Raincloud'),
        html.Hr(),
        dcc.Graph(id='Trinity_Raincloud'),
        html.Button('Download Raincloud TransPi', id='download-Raincloud-TransPi', n_clicks=0),
        html.Button('Download Raincloud Trinity', id='download-Raincloud-Trinity', n_clicks=0),
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_alignment= html.Div(
    [
        dbc.Row(html.H1("Alignment of Buscos")),
        #TODO add styling and css to center correctly
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="busco_name_selector",
                        options=get_busco_genes(),
                        placeholder="Select Busco Gene by Name",
                    ),
                ],
            ),
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="busco_function_selector",
                        options=get_busco_functions(),
                        placeholder="Select Busco Gene by Function",
                    ),
                ],
            ),
        ),
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Dropdown(
                        id="type_selector",
                        options=[
                            {"label": "single", "value": "single"},
                            {"label": "fragmented", "value": "fragmented"},
                            {"label": "duplicated", "value": "duplicated"},
                        ],
                        placeholder="Select what Type of Busco Gene to show",
                    ),
                ],
            )
        ),
        #TODO add download options

        #TODO
        #1 selector by busco name
        #2 selector by function
        #select single,fragmented, duplicated
        #TODO Add tree view

        #TODO visualize alignment
            #dcc.Graph(id='Busco_alignment'),
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
                dbc.Tab(tab_alignment, label="Busco Alignment", tab_id="tab_alignment"),
            ],
        ),
        html.Div(id="tab-content", style={"marginBottom": "10px"}),
    ]
)
#----------------------------------------------------------

