# Organize the various tabs
#----------------------------------------------------------
import dash_bootstrap_components as dbc
from dash import dcc, html
from pages.components.user_selection import get_busco_genes, get_busco_functions
from pages.components.alignment_functions import alignment_data
import dash_bio as dashbio
#----------------------------------------------------------
#TODO for each tab add download buttons
#----------------------------------------------------------
def create_transcriptome_selector(id):
    return dbc.Col(
        [
            dbc.Card(
                dbc.CardBody(
                    dcc.Dropdown(
                        id=id,
                        options=[
                            {"label": "Protein", "value": "Protein"},
                            {"label": "TransPi", "value": "TransPi"},
                            {"label": "Trinity", "value": "Trinity"},
                        ],
                        multi=True,
                        placeholder="Select transciptome",
                    )
                ),
            )
        ],
        width=2,
    )

#----------------------------------------------------------
tab_heatmap = html.Div(
    [
        dbc.Row(
            html.H1("Species v. Buscos Heatmap"),
        ),
        dbc.Row(
            [
                #selector to switch between the Protein and the transpi/trinity
                create_transcriptome_selector("heatmap_selector"),
                #empty place holder
                dbc.Col(
                    width=1
                ),
                #select whether to show the difference
                dbc.Col(
                    [
                        dbc.Switch(
                            id="difference_switch",
                            label=dbc.Label("Show difference Heatmap", style={"font-size": "20px"}),
                            value=True,
                            style={
                                "display": "block",
                                "margin": "20px",
                                "transform": "scale(1.4)",
                            },
                        )
                    ],width=2,
                ),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    html.Div(id='busco_heatmap'),
                    html.Hr(),
                ],
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    # html.Button('Download Heatmap', id='download-heatmap'),
                    # html.Button('Download Difference Heatmap', id='download-difference-heatmap', n_clicks=0),
                ],
            ),
        ),
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_stacked_area= html.Div(
    [
        dbc.Row(html.H1("Stacked Area Plots")),
        dbc.Row(
            [
                create_transcriptome_selector("Stacked_area_selector"),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    #stacked area plots
                    html.Div(id='Stacked_area'),
                    html.Hr(),
                ],
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    # html.Button('Download Stacked Area TransPi', id='download-stacked-area-TransPi', n_clicks=0),
                    # html.Button('Download Stacked Area Trinity', id='download-stacked-area-Trinity', n_clicks=0),
                ],
            ),
        ),  
    ],
    className="mt-3",
)
#----------------------------------------------------------
tab_raincloud= html.Div(
    [
        dbc.Row(html.H1("TransPi v. Trinity Raincloud Plots")),
        html.Hr(),
        dbc.Row(
            [
                create_transcriptome_selector("Raincloud_selector"),
            ]
        ),
        dbc.Row(
            dbc.Col(
                [
                    #Raincloud plots
                    html.Div(id='Rainclouds'),
                    html.Hr(),
                ],
            ),
        ),
        dbc.Row(
            dbc.Col(
                [
                    # html.Button('Download Raincloud Protein', id='download-Raincloud-Protein', n_clicks=0),
                    # html.Button('Download Raincloud TransPi', id='download-Raincloud-TransPi', n_clicks=0),
                    # html.Button('Download Raincloud Trinity', id='download-Raincloud-Trinity', n_clicks=0),
                ],
            ),
        ),  
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
                #TODO is this worth keeping? 
                #If we only look at 1 busco gene at a time, do we even need this?
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
                dbc.Col(
                    html.Div(
                        [
                            dashbio.AlignmentChart(
                                id="alignment_viewer",
                                data=alignment_data,
                                height=700,
                                width=1600,
                                tilewidth=30, 
                            ),
                            
                        ]
                    ),
                ),
                #TODO Add tree view
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # html.Button('Download Raw Alignment', id='download-Raw-Alignment', n_clicks=0),
                        # html.Button('Download Alignment Figure', id='download-Alignment-Figure', n_clicks=0),
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
            active_tab="tab_heatmap",
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

