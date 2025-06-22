# Organize the various tabs
#----------------------------------------------------------
import dash_bootstrap_components as dbc
from dash import dcc, html
from .user_selection import get_busco_genes
from .alignment_functions import alignment_data
import dash_bio as dashbio
#----------------------------------------------------------
#TODO for each tab add download buttons
#----------------------------------------------------------
#function to create radio buttons (as replacement for selectors)
#input list of values to be created
def create_checklist(id, cl_width, to_create, default_value):
    #generate options
    new_options = []
    for i in to_create:
        #print("create ", i)
        new_options.append({'label': f'{i}', 'value': f'{i}'})
                           
    #set default to empty if None
    if default_value is None:
        default_value = []
     
    return dbc.Col(
        [
            dcc.Checklist(
                id=id,
                options=new_options,
                value=[default_value],
                inline=True,
                inputStyle={"margin-left": "20px"},
                style={'width':'100%'},
            ),
        ],
        width=cl_width,
    )
#----------------------------------------------------------
#update species buttons per tab
def create_update_button(tab_id):
    return html.Div([
        html.Button('Update Plots', id=f'update_species_button_{tab_id}', n_clicks=0)
    ])
#----------------------------------------------------------
tab_heatmap = html.Div(
    [
        dbc.Row(
            [
            dbc.Col(
                [
                html.H1("Species v. Buscos Heatmap"),
                ], width=10,
            ),
            dbc.Col(
                [
                create_update_button('heatmap'),
                ], width=2,
            )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                dcc.Textarea(
                    id='user_full_table_input',
                    value='''
                        Input the contents of the BUSCO full table with all genes below with matching format to this:\n
                        # BUSCO version is: 4.1.4 
                        # The lineage dataset is: metazoa_odb10 (Creation date: 2020-09-10, number of species: 65, number of BUSCOs: 954)
                        # Busco id	Status	Sequence	Score	Length
                        5951at33208a	Duplicated	TRINITY_DN496_c0_g1_i7	2497.0	1125
                        5951at33208a	Duplicated	SPADES.k25.NODE_765_length_4786_cov_39.834489_g517_i1	2454.6	1105
                        ''',
                    style={'width': '50%', 'height': 100},
                ),
                html.Button('Submit data', id='submit_full_table_button', n_clicks=0),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                #selector to switch between the Protein and the transpi/trinity
                create_checklist("heatmap_selector", 10, ['Protein', 'TransPi', 'Trinity', 'Show difference heatmap'], 'Protein'),
                #empty place holder
                dbc.Col(
                    width=1
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
    ]
)
#----------------------------------------------------------
tab_stacked_area= html.Div(
    [
        dbc.Row(
            [
            dbc.Col(
                [
                html.H1("Stacked Area Plots"),
                ], width=10
            ),
            dbc.Col(
                [
                create_update_button('stacked_area'),
                ], width=2
            ),
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                #create_transcriptome_selector("Stacked_area_selector"),
                create_checklist("Stacked_area_selector", 10, ['Protein', 'TransPi', 'Trinity', 'Log Comparison of Trinity vs TransPi'], 'Protein'),
                html.Hr(),
            ]
        ),
        #call when comparison is selected
        html.Div(id="busco_type_selector_area_component", children=[]),
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
        dbc.Row(
            [
            dbc.Col(
                [
                html.H1("TransPi v. Trinity Raincloud Plots"),
                ], width=10,
            ),
            dbc.Col(
                [
                create_update_button('raincloud'),
                ], width=2,
            )
            ]
        ),
        html.Hr(),
        dbc.Row(
            [
                create_checklist("Raincloud_selector", 10, ['Protein', 'TransPi', 'Trinity'], 'Protein'),
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
        dbc.Row(
            [
            dbc.Col(
                [
                html.H1("Alignment of Buscos"),
                ], width=10,
            ),
            dbc.Col(
                [
                create_update_button('alignment'),
                ], width=2,
            )
            ]
        ),
        html.Hr(),
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
                                dcc.RadioItems(id = 'type_selector', options=['single', 'duplicated'], inputStyle={"margin-left": "20px"}, value='single', inline=True),
                                #create_checklist("type_selector", 5, ['single', 'duplicated'], 'single'),
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
                    dbc.Alert(
                        "No Matches found!",
                        id="user_alert_none_found",
                        is_open=False,
                        dismissable=True,
                    ),
                    ]
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
                        ],
                    ),
                ),
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