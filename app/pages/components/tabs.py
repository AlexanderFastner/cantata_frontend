# Organize the various tabs
#----------------------------------------------------------
import dash_bootstrap_components as dbc
from dash import dcc, html
from pages.components.user_selection import get_busco_genes, get_busco_functions
from pages.components.Busco_comparison import Alignment_df
import dash_bio as dashbio
#----------------------------------------------------------
#TODO for each tab add download buttons
#----------------------------------------------------------
tab_heatmap = html.Div(
    [
        html.H1("Species v. Buscos Heatmap"),
        #selector to switch between the Protein buscos and the transpi/trinity ones
        dbc.Col(
            [
                dbc.Card(
                    dbc.CardBody(
                        dcc.Dropdown(
                            id="heatmap_selector",
                            options=["Protein","TransPi","Trinity"],
                            multi=True,
                            placeholder="Select transciptome",
                        )
                    ),
                )
            ],width=2,
        ),
        dbc.Col(
            [
                dcc.Graph(id='busco_heatmap'),
                html.Hr(),
                #TODO dif heatmp is the difference calculated betweeen the different heatmaps to more easily spot differences
                #TODO dcc.Graph(id='busco_difference_heatmap'),
            ],
        ),
        dbc.Col(
            [
                html.Button('Download Heatmap', id='download-heatmap'),
                html.Button('Download Difference Heatmap', id='download-difference-heatmap', n_clicks=0),
            ],
        ),
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
        html.H1("Alignment of Buscos"),
        #TODO add styling and css to center correctly
        dbc.Row(
            [
                dbc.Col(
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
                ),
                
                dbc.Col( 
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
                ),
                dbc.Col(
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
                ),
            ],
            style={"width":"100%"},
        ),
        dbc.Row(
            [
                #TODO visualize alignment heatmap 
                dbc.Col(
                    html.Div(
                        [
                            #TODO fix this somehow
                            #TODO get 3 letter code dict from molpal excel sheet
                            dashbio.AlignmentChart(id="alignment_viewer", data=Alignment_df, height=800, tilewidth=40)
                        ]
                    ),
                ),
                #TODO Add tree view

                #TODO add download options
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.Button('Download Raw Alignment', id='download-Raw-Alignment', n_clicks=0),
                        html.Button('Download Alignment Figure', id='download-Alignment-Figure', n_clicks=0),
                    ], width=4,
                )
            ],
        ),
    ],
    #style={'display': 'inline-block'},
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

