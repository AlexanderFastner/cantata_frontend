# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as ex

from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from flask import send_file

import sys
sys.path.append("/wd/app/pages")
print(sys.path)

import pages.components.user_selection as user_selection
import pages.components.tabs as tabs
import pages.components.alignment_functions as alignment_functions
#----------------------------------------------------------
dash.register_page(__name__, path="/Busco")
#----------------------------------------------------------
# On startup
user_selection.read_species_list(),
#print(user_selection.species,flush=True),
#----------------------------------------------------------
layout = html.Div(
    [
        dbc.Row( #top level row
            [
                dbc.Col( #left column for selection
                    [
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5("Select Group for comparison")),
                                dbc.CardBody(
                                    [
                                        #TODO when new data is added you need to update group_options and species!
                                        dcc.Dropdown(
                                            id="group_dropdown",
                                            options=user_selection.group_options,
                                            value=[],
                                            placeholder="Select a Group",
                                        ),
                                    ],
                                ),
                            ], style={'width': '100%', 'height': '13vh'}
                        ),
                        #this is for users uploading their own data
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5("Input your Busco results")),
                                dbc.CardBody(
                                    [
                                        #TODO add callbacks for these
                                        dcc.Input(
                                            id="species_name_input",
                                            type='text',
                                            placeholder="Your species name here!",
                                        ),
                                        dcc.Textarea(
                                            id='user_busco_textarea',
                                            value='Input the contents of the BUSCO short summary results here\n',
                                            style={'width': '100%', 'height': 100},
                                        ),
                                        html.Button('Submit data', id='submit_species_button', n_clicks=0),
                                    ],
                                ),
                            ], style={'width': '100%', 'height': '26vh'}
                        ),
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H5("Select Individual Species")),
                                dbc.CardBody(
                                    [
                                        dcc.Checklist(
                                            id='species_selected',
                                            options=user_selection.species,
                                            value=['None']
                                        ), 
                                    ],
                                ),
                            ], style={'width': '100%', 'height': '70vh', 'overflow': 'scroll', 'display': 'inline-block'},
                        ),
                    ], style={"max-width": "20%", 'padding-bottom': '60px'},                    
                ),

                dbc.Col( # middle/right column for plotting
                    #tabs for the various possible plots
                    [
                        tabs.plot_selector_tabs
                    ],
                    style={"width": "80%", 'height' : 'auto'},
                ),
            ],
        ),

    ],
    style={"width": "100%", 'display': 'inline-block'}
)
#----------------------------------------------------------
#Callbacks
#----------------------------------------------------------
#species checklist
@callback(
    Output('species_selected', 'value'),
    Input('group_dropdown', 'value'),
    prevent_initial_call=True,
)
def update_checklist_options(group_value):
    print("update checklist values: ", group_value)
    updated_options = []
    if group_value == "All":
        updated_options = user_selection.species
        print("all detected", updated_options, flush=True)
        return updated_options
    if 'All' in group_value:
        print("second detect")

    #update so when Clear Selection is selected everything is removed
    if "None" in group_value:
        updated_options=[]
        group_value=""
        return updated_options
    
    #convert from , seperated string into array of strings
    if group_value is not [] and group_value is not None:
        updated_options = group_value.split(',')
        #print("updated_options: ", updated_options)
        return updated_options
    else:
        return []
#----------------------------------------------------------
#make layout for busco_type_selector (off by default)
#multi selector to choose what to track in Trinity vs TransPi
@callback(
    Output('busco_type_selector_area_component', 'children'),
    Input('Stacked_area_selector', 'value'),
    prevent_initial_call=True,
)
def show_type_selector(type):
    print("called", flush=True)
    if 'Log Comparison of Trinity vs TransPi' in type:
        print('reached creation', flush=True)
        return html.Div(
            [
                dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H2("Select type of Busco to show in Comparison"),
                            tabs.create_checklist("busco_type_selector_area", 10, ['Complete_&_single-copy', 'Complete_&_duplicated', 'Fragmented', 'Missing', 'All'], 'All'),
                        ],width=10
                    ),
                ],
                ),
                html.Hr(),
            ],
            id="busco_type_selector_area_component",
        )
    else:
        return html.Div(id="busco_type_selector_area_component", children=[])
#----------------------------------------------------------
#User input
#TODO fix error that stops page from loading!
#Add new checklist box for that species that toggles its inclusion in plots

# @callback(
#     Output(component_id="species_selected", component_property="value"),
#     State(component_id="species_name_input", component_property="value"),
#     State(component_id="user_busco_textarea", component_property="value"),
#     Input(component_id="submit_species_button", component_property="n_clicks"),
# )
# def read_user_data(species_name_input, user_busco_textarea, submit_species_button):
#     #TODO sanitize data!!!
#     print("species_name_input: ", species_name_input, flush=True)
#     print("user_busco_textarea: ", user_busco_textarea, flush=True)
#     new_species={"label": f"{species_name_input}","value": f"{user_busco_textarea}"}
#     user_selection.group_options.insert(0, new_species)
    
#     return update_checklist_options(new_species)

#----------------------------------------------------------
#Heatmaps
#----------------------------------------------------------
#Heatmap selector for which dataset you want.
@callback(
    Output(component_id="busco_heatmap", component_property="children"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="heatmap_selector", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button_heatmap", component_property="n_clicks"),
    prevent_initial_call=True
)
def get_heatmap_df(species_selected, heatmap_selector, active_tab, update_species_button):
    if "tab_heatmap" not in active_tab:
        return html.P("Not active")
    fig_array=[]
    #filter by user selection
    if species_selected != None and species_selected !=[] and heatmap_selector is not None and heatmap_selector != "None":
        #check which dataset the user wants to see
        for selected in heatmap_selector: 
            if selected == "Protein":
                fig_array.append("Protein_heatmap")
            elif selected == "Trinity":
                fig_array.append("Trinity_heatmap")
            elif selected == "TransPi":
                fig_array.append("TransPi_heatmap")
            elif selected == "Show difference heatmap":
                fig_array.append("Difference_heatmap")
    else:
        return None
    
    #alwyas add diff to front of list
    if "Difference_heatmap" in fig_array and len(fig_array) < 3:
        fig_array.remove("Difference_heatmap")
    if "Difference_heatmap" in fig_array:
        fig_array.remove("Difference_heatmap")
        fig_array.insert(0, "Difference_heatmap")
    
    print(fig_array, flush=True)
    print()
    #return Div with figures and names
    #add callbacks that those newly created graph ids get updated
    #add dcc.Graph elements to array and return child
    child = []
    if fig_array == []:
        fig_array.append("None")
    for fig in fig_array:
        #update children of output
        child.append(dcc.Graph(id=fig))
    return child

#TODO fix/implement this button for each heatmap
# @callback(
#     Output('heatmap', 'config'),
#     Input('download-heatmap', 'n_clicks'),
#     State('busco_heatmap', 'figure')
# )
# def download_heatmap(n_clicks, figure):
#     if n_clicks is not None and n_clicks > 0:
#         print("HEATMAP DOWNLOAD")
#         # Save the current figure as a .png image
#         pio.write_image(figure, 'heatmap.png')
#         print("wrote image")
#         # Send the file to the client
#         return send_file('heatmap.png')
#----------------------------------------------------------
#for each item in children
    #compute the difference between the other heatmaps
    #update that dynamic div
@callback(
    Output(component_id="Difference_heatmap", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="busco_heatmap", component_property="children"),
)
def update_Difference(species_selected, children):
    #for everything in children get the heatmap_df
    #after this find a way to calculate the difference between all these
    Prot_subset = None
    Trinity_subset = None
    TransPi_subset = None
    diff = False
    for item in children:
        #print(item)
        if "Protein_heatmap" in item.get("props").get("id"):
            Prot_heatmap_df = pd.read_csv('/wd/data/busco5_full_table_Proteome_df_numbers.csv', index_col=0)
            Prot_subset = Prot_heatmap_df.loc[Prot_heatmap_df.index.isin(species_selected)]
        if "Trinity_heatmap" in item.get("props").get("id"):
            Trinity_heatmap_df = pd.read_csv('/wd/data/busco4_full_table_Trinity_df_numbers.csv', index_col=0)
            Trinity_subset = Trinity_heatmap_df.loc[Trinity_heatmap_df.index.isin(species_selected)]
        if "TransPi_heatmap" in item.get("props").get("id"):
            TransPi_heatmap_df = pd.read_csv('/wd/data/busco4_full_table_TransPi_df_numbers.csv', index_col=0)
            TransPi_subset = TransPi_heatmap_df.loc[TransPi_heatmap_df.index.isin(species_selected)]
        if "Difference_heatmap" in item.get("props").get("id"):
            diff = True
        
    if not diff:
        return None
    #difference between all 3
    diff_df = None
    if Prot_subset is not None and Trinity_subset is not None and TransPi_subset is not None:
        diff1 = pd.DataFrame(np.where(Prot_subset == Trinity_subset, 1, 0), columns=Prot_subset.columns, index=Prot_subset.index)
        diff2 = pd.DataFrame(np.where(Prot_subset == TransPi_subset, 1, 0), columns=Prot_subset.columns, index=Prot_subset.index)
        diff_df = pd.DataFrame(np.where(diff1 == diff2, 1, 0), columns=diff1.columns, index=diff1.index)
        #print("all3", diff_df)
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Diff plot  "),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig
        
    #difference between 2
    elif Prot_subset is not None and Trinity_subset is not None:
        diff_df = pd.DataFrame(np.where(Prot_subset==Trinity_subset,1,0),columns=Prot_subset.columns, index=Prot_subset.index) 
        #print("Prot Trin", diff_df)
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Diff plot  "),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig
    elif Trinity_subset is not None and TransPi_subset is not None:
        diff_df = pd.DataFrame(np.where(Trinity_subset==TransPi_subset,1,0),columns=Trinity_subset.columns, index=Trinity_subset.index) 
        #print("Trin Trans", diff_df)
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Diff plot  "),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig
    elif Prot_subset is not None and TransPi_subset is not None:
        diff_df = pd.DataFrame(np.where(Prot_subset==TransPi_subset,1,0),columns=Prot_subset.columns, index=Prot_subset.index) 
        #print("Prot Trans", diff_df)   
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Diff plot  "),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig    
    
    print("should never get here (update difference error)")
    return None

#----------------------------------------------------------
#update Protein fig if selected
@callback(
    Output(component_id="Protein_heatmap", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="busco_heatmap", component_property="children"),
)
def update_Protein(species_selected, children):
    for item in children:
        if "Protein_heatmap" in item.get("props").get("id"):
            heatmap_df = pd.read_csv('/wd/data/busco5_full_table_Proteome_df_numbers.csv', index_col=0)
            subset = heatmap_df.loc[heatmap_df.index.isin(species_selected)]
            Protein_fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF"], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
            Protein_fig.update_xaxes(showticklabels=False)
            Protein_fig.update_layout(title="Protein Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
            return Protein_fig
    else:
        return None
#----------------------------------------------------------
#update Trinity fig if selected
@callback(
    Output(component_id="Trinity_heatmap", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="busco_heatmap", component_property="children"),
)
def update_Trinity(species_selected, children):
    for item in children:
        if "Trinity_heatmap" in item.get("props").get("id"):
            heatmap_df = pd.read_csv('/wd/data/busco4_full_table_Trinity_df_numbers.csv', index_col=0)
            subset = heatmap_df.loc[heatmap_df.index.isin(species_selected)]
            Trinity_fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF"], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
            Trinity_fig.update_xaxes(showticklabels=False)
            Trinity_fig.update_layout(title="Trinity Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
            return Trinity_fig
    else:
        return None
#----------------------------------------------------------
#update TransPi fig if selected
@callback(
    Output(component_id="TransPi_heatmap", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="busco_heatmap", component_property="children"),
)
def update_TransPi(species_selected, children):
    for item in children:
        if "TransPi_heatmap" in item.get("props").get("id"):
            heatmap_df = pd.read_csv('/wd/data/busco4_full_table_TransPi_df_numbers.csv', index_col=0)
            subset = heatmap_df.loc[heatmap_df.index.isin(species_selected)]
            TransPi_fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF"], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
            TransPi_fig.update_xaxes(showticklabels=False)
            TransPi_fig.update_layout(title="TransPi Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
            return TransPi_fig
    else:
        return None
#----------------------------------------------------------    
#Stacked Area plots       
#----------------------------------------------------------
#Variables
color_map = {"Complete_BUSCOs": "#785EF0",
                    "Complete_&_single-copy": "#648FFF",
                    "Complete_&_duplicated" : "#DC267F",
                    "Fragmented":"#FE6100",
                    "Missing":"#FFB000"
                    }
#----------------------------------------------------------
#Dynamicly generate Stacked Area plots  
@callback(
    Output(component_id="Stacked_area", component_property="children"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area_selector", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button_stacked_area", component_property="n_clicks"),
    prevent_initial_call=True
)     
def get_stacked_area(species_selected, Stacked_area_selector, active_tab, update_species_button):
    if "tab_stacked_area" not in active_tab:
        return html.P("Not active (This shouldn't happen)") 
    fig_array=[]
    print(species_selected, Stacked_area_selector, active_tab, update_species_button)
    print(flush=True)
    #filter by user selection
    if 'None' in species_selected: 
        if len(species_selected) < 2:
            print("Please select a species, current species selected is None", flush=True)
            return None
        else:
            #print("old list: ", species_selected, flush=True)
            species_selected.remove('None')
            #print("new list: ", species_selected, flush=True)

    if species_selected != None and species_selected !=[] and Stacked_area_selector != "None" and Stacked_area_selector is not None:
        #check which dataset the user wants to see
        for selected in Stacked_area_selector:   
            #print("selected", selected)
            if selected == "Protein":
                fig_array.append("Protein_stacked_area")
            elif selected == "Trinity":
                fig_array.append("Trinity_stacked_area")
            elif selected == "TransPi":
                fig_array.append("TransPi_stacked_area")
            #if selected put difference to the front of the list
            elif selected == "Log Comparison of Trinity vs TransPi":
                fig_array = ["Log_Comparison_of_Trinity_vs_TransPi"] + fig_array
                print("added")
                print(fig_array)
    else:
        print("missing selection Stacked area")
        return None

    child = []
    if fig_array == []:
        fig_array.append("None")
    print("area, ", fig_array)
    for fig in fig_array:
        #update children of output
        child.append(dcc.Graph(id=fig))
    print(child, flush=True)
    return child
#----------------------------------------------------------
#Protein area
@callback(
    Output(component_id="Protein_stacked_area", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area", component_property="children"),
)
def update_Protein_area(species_selected, children):
    for item in children:
        print(item, flush=True)
        if "Protein_stacked_area" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                Protein_area_df = pd.read_csv('/wd/data/busco5_short_summary_Proteome.tsv', sep="\t", index_col=0)
                Protein_area_df = Protein_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                subset_Protein = Protein_area_df.loc[Protein_area_df.index.isin(species_selected)]
                fig = go.Figure(data=ex.area(subset_Protein, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                                title="Protein"))
                print("finished fig", flush=True)
                return fig
            else:
                fig = None
                return fig
    else:
        return None
#----------------------------------------------------------       
#Trinity area
@callback(
    Output(component_id="Trinity_stacked_area", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area", component_property="children"),
)
def update_Trinity_area(species_selected, children):
    #filter by user selection
    for item in children:
        if "Trinity_stacked_area" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                #print("Trinity", species_selected)
                Trinity_area_df = pd.read_csv('/wd/data/busco4_short_summary_Trinity.tsv', sep="\t", index_col=0)
                Trinity_area_df = Trinity_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                subset_Trinity = Trinity_area_df.loc[Trinity_area_df.index.isin(species_selected)]
                #print(subset_Trinity)
                fig = go.Figure(data=ex.area(subset_Trinity, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                                title="Trinity"))
                return fig
            else:
                fig = None
                return fig
    else:
        return None

#TODO fix button
# @callback(
#     Output('busco_stacked_area_Trinity', 'config'),
#     Input('download-stacked-area-Trinity', 'n_clicks'),
#     State('Trinity_area', 'figure')
# )
# def download_stacked_area_Trinity(n_clicks, figure):
#     if n_clicks is not None and n_clicks > 0:
#         # Save the current figure as a .png image
#         pio.write_image(figure, 'Trinity_stacked_area.png')
#         print("wrote Trinity stacked")
#         # Send the file to the client
#         return send_file('Trinity_stacked_area.png')
#----------------------------------------------------------
#TransPi area
@callback(
    Output(component_id="TransPi_stacked_area", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area", component_property="children"),
)
def update_TransPi_area(species_selected, children):
    #print("species_selected ",species_selected)
    for item in children:
        if "TransPi_stacked_area" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                TransPi_area_df = pd.read_csv('/wd/data/busco4_short_summary_TransPi.tsv', sep="\t", index_col=0)
                TransPi_area_df = TransPi_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                subset_TransPi = TransPi_area_df.loc[TransPi_area_df.index.isin(species_selected)]
                fig = go.Figure(data=ex.area(subset_TransPi, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                                title="TransPi"))
                return fig
            else:
                fig = None
                return fig
    else:
        return None

#TODO fix button
# @callback(
#     Output('busco_stacked_area_TransPi', 'config'),
#     Input('download-stacked-area-TransPi', 'n_clicks'),
#     State('TransPi_area', 'figure')
# )
# def download_stacked_area_TransPi(n_clicks, figure):
#     if n_clicks is not None and n_clicks > 0:
#         # Save the current figure as a .png image
#         pio.write_image(figure, 'TransPi_stacked_area.png')
#         print("wrote TransPi stacked")
#         # Send the file to the client
#         return send_file('TransPi_stacked_area.png')
#----------------------------------------------------------
#log comparison of Trinity TransPi
@callback(
    Output(component_id="Log_Comparison_of_Trinity_vs_TransPi", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area", component_property="children"),
    Input(component_id="busco_type_selector_area", component_property="value"),
)
def update_Trinity_TransPi_area(species_selected, children, busco_type_selector_area):
    print('update log comparison', flush=True)
    print("species_selected ",species_selected, flush=True)
    print("children ",children, flush=True)
    for item in children:
        if "Log_Comparison_of_Trinity_vs_TransPi" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                TransPi_area_df = pd.read_csv('/wd/data/busco4_short_summary_TransPi.tsv', sep="\t", index_col=0)
                Trinity_area_df = pd.read_csv('/wd/data/busco4_short_summary_Trinity.tsv', sep="\t", index_col=0)
                TransPi_area_df = TransPi_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                Trinity_area_df = Trinity_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                #format of subsets
                # species_name  Complete_&_single-copy	Complete_&_duplicated	Fragmented	Missing
                # species1      100 50  40  10
                # species2      140 10  30  20
                subset_TransPi = TransPi_area_df.loc[TransPi_area_df.index.isin(species_selected)]
                subset_Trinity = Trinity_area_df.loc[Trinity_area_df.index.isin(species_selected)]
                barplot_df = pd.DataFrame(np.log2(subset_Trinity.values / subset_TransPi.values), index=subset_TransPi.index, columns=subset_TransPi.columns)
                # print(barplot_df)
                #format for barplot
                # species name   Complete_&_single-copy  Complete_&_duplicated  Fragmented  Missing
                #species1        log2(Trinity.value/TransPi.value) value value value
                #species2        value value value value
                #...

                #subset by selected type
                # print(busco_type_selector_area)
                if "All" not in busco_type_selector_area:
                    barplot_df = barplot_df[busco_type_selector_area]
                if len(busco_type_selector_area) == 0:
                    fig = None
                    return fig
                fig = go.Figure()
                for col in barplot_df.columns:
                    fig.add_trace(go.Bar(x=barplot_df.index, y=barplot_df[col], name=col))
                
                fig.update_layout(
                    title='Log2 difference Trinity vs TransPi (Trinity on Top)',
                    xaxis_title='Species',
                    yaxis_title='Log2',
                    barmode='group'
                )
                return fig
            
            else:
                print("never get here")
                return None
    else:
        print("no comp in children")
        return None
#----------------------------------------------------------
#Raincloud selection
#----------------------------------------------------------
#Dynamicly generate Rainclouds
@callback(
    Output(component_id="Rainclouds", component_property="children"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Raincloud_selector", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button_raincloud", component_property="n_clicks"),
    prevent_initial_call=True
)
def get_Rainclouds(species_selected, Raincloud_selector, active_tab, update_species_button):
    if "tab_raincloud" not in active_tab:
        return html.P("Not active")
    fig_array=[]
    #filter by user selection
    #print("raincloud: ", species_selected)
    if species_selected is not None and species_selected !=[] and Raincloud_selector != "None" and Raincloud_selector is not None:
        #check which dataset the user wants to see
        for selected in Raincloud_selector:   
            if selected == "Protein":
                fig_array.append("Protein_raincloud")
            elif selected == "Trinity":
                fig_array.append("Trinity_raincloud")
            elif selected == "TransPi":
                fig_array.append("TransPi_raincloud")
    else:
        return None

    child = []
    if fig_array == []:
        fig_array.append("None")
    for fig in fig_array:
        #update children of output
        child.append(dcc.Graph(id=fig))
    return child
#----------------------------------------------------------
#Raincould Protein
@callback(
    Output(component_id="Protein_raincloud", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Rainclouds", component_property="children"),
)
def update_Protein_Raincloud(species_selected, children):
    #filter by user selection
    for item in children:
        if "Protein_raincloud" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                Protein_df = pd.read_csv('/wd/data/busco5_short_summary_Proteome.tsv', sep="\t", index_col=0)
                subset_Protein = Protein_df.loc[Protein_df.index.isin(species_selected)]

                #data wrangling
                Protein_column_names = subset_Protein.columns.to_list()[:-1]
                all_column_values=[]
                for column in Protein_column_names:
                    column_values_Protein = subset_Protein[column].values
                    all_column_values.append(column_values_Protein)
                #Construct Plot
                fig = go.Figure()

                data = []
                for i in range(len(Protein_column_names)):
                    data.append(go.Violin(x=all_column_values[i], name=Protein_column_names[i], meanline_visible=True, opacity=0.4, fillcolor=color_map.get(Protein_column_names[i]), line=dict(color=color_map.get(Protein_column_names[i])), side='positive'))
                    # Scatter
                    # Build (x,y) pairs for each category
                    fig = go.Figure(data=data)

                for values, category in zip(all_column_values, Protein_column_names):
                    c = [category for _ in range(len(values))]
                    fig.add_trace(go.Scatter(x=values, y=c, mode='markers', showlegend=False, marker=dict(color=color_map.get(category)), text=subset_Protein.index.tolist()))
                
                fig.update_layout(title='Protein Raincloud Plot of BUSCOs Data',
                                xaxis_title='Counts',
                                xaxis=dict(range=[0, None]),
                                hovermode='closest')
                return fig
            else:
                fig = None
                return fig
#----------------------------------------------------------
#Raincloud TransPi
@callback(
    Output(component_id="TransPi_raincloud", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Rainclouds", component_property="children"),
)
def update_TransPi_Raincloud(species_selected, children):
    #filter by user selection
    for item in children:
        if "TransPi_raincloud" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                TransPi_df = pd.read_csv('/wd/data/busco4_short_summary_TransPi.tsv', sep="\t", index_col=0)
                subset_TransPi = TransPi_df.loc[TransPi_df.index.isin(species_selected)]

                #data wrangling
                TransPi_column_names = subset_TransPi.columns.to_list()[:-1]
                all_column_values=[]
                for column in TransPi_column_names:
                    column_values_TransPi = subset_TransPi[column].values
                    all_column_values.append(column_values_TransPi)
                #Construct Plot
                fig = go.Figure()

                data = []
                for i in range(len(TransPi_column_names)):
                    data.append(go.Violin(x=all_column_values[i], name=TransPi_column_names[i], meanline_visible=True, opacity=0.4, fillcolor=color_map.get(TransPi_column_names[i]), line=dict(color=color_map.get(TransPi_column_names[i])), side='positive'))
                    # Scatter
                    # Build (x,y) pairs for each category
                    fig = go.Figure(data=data)
                for values, category in zip(all_column_values, TransPi_column_names):
                    c = [category for _ in range(len(values))]
                    fig.add_trace(go.Scatter(x=values, y=c, mode='markers', showlegend=False, marker=dict(color=color_map.get(category)), text=subset_TransPi.index.tolist()))
                
                fig.update_layout(title='TransPi Raincloud Plot of BUSCOs Data',
                                xaxis_title='Counts',
                                xaxis=dict(range=[0, None]),
                                hovermode='closest')
                return fig
            else:
                fig = None
                return fig

#TODO fix button
# @callback(
#     Output('busco_Raincloud_TransPi', 'config'),
#     Input('download-Raincloud-TransPi', 'n_clicks'),
#     State('TransPi_Raincloud', 'figure')
# )
# def download_Raincloud_TransPi(n_clicks, figure):
#     if n_clicks is not None and n_clicks > 0:
#         # Save the current figure as a .png image
#         pio.write_image(figure, 'TransPi_Raincloud.png')
#         print("wrote TransPi Raincloud")
#         # Send the file to the client
#         return send_file('TransPi_stacked_area.png')
#----------------------------------------------------------      
#Raincloud Trinity
@callback(
    Output(component_id="Trinity_raincloud", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Rainclouds", component_property="children"),
)
def update_Trinity_Raincloud(species_selected, children):
    #filter by user selection
    for item in children:
        if "Trinity_raincloud" in item.get("props").get("id"):
            if species_selected != None and species_selected !=[]:
                Trinity_df = pd.read_csv('/wd/data/busco4_short_summary_Trinity.tsv', sep="\t", index_col=0)
                subset_Trinity = Trinity_df.loc[Trinity_df.index.isin(species_selected)]

                #data wrangling
                Trinity_column_names = subset_Trinity.columns.to_list()[:-1]
                all_column_values=[]
                for column in Trinity_column_names:
                    column_values_Trinity = subset_Trinity[column].values
                    all_column_values.append(column_values_Trinity)
                #Construct Plot
                fig = go.Figure()

                data = []
                for i in range(len(Trinity_column_names)):
                    data.append(go.Violin(x=all_column_values[i], name=Trinity_column_names[i], meanline_visible=True, opacity=0.4, fillcolor=color_map.get(Trinity_column_names[i]), line=dict(color=color_map.get(Trinity_column_names[i])), side='positive'))
                    # Scatter
                    # Build (x,y) pairs for each category
                    fig = go.Figure(data=data)
                for values, category in zip(all_column_values, Trinity_column_names):
                    c = [category for _ in range(len(values))]
                    fig.add_trace(go.Scatter(x=values, y=c, mode='markers', showlegend=False, marker=dict(color=color_map.get(category)), text=subset_Trinity.index.tolist()))
                
                fig.update_layout(title='Trinity Raincloud Plot of BUSCOs Data',
                                xaxis_title='Counts',
                                xaxis=dict(range=[0, None]),
                                hovermode='closest')
                return fig
            else:
                fig = None
                return fig

#TODO fix button
# @callback(
#     Output('busco_Raincloud_Trinity', 'config'),
#     Input('download-Raincloud-Trinity', 'n_clicks'),
#     State('Trinity_Raincloud', 'figure')
# )
# def download_Raincloud_Trinity(n_clicks, figure):
#     if n_clicks is not None and n_clicks > 0:
#         # Save the current figure as a .png image
#         pio.write_image(figure, 'Trinity_Raincloud.png')
#         print("wrote Trinity Raincloud")
#         # Send the file to the client
#         return send_file('Trinity_stacked_area.png')

#---------------------------------------------------------- 
#Alignment
#----------------------------------------------------------
@callback(
    [
    Output(component_id="alignment_viewer", component_property="data"),
    Output(component_id="user_alert_none_found", component_property="is_open")
    ],
    State(component_id="species_selected", component_property="value"),
    Input(component_id="busco_name_selector", component_property="value"),
    Input(component_id="type_selector", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button_alignment", component_property="n_clicks"),
    prevent_initial_call=True
)
def update_align(species_selected, busco_name_selector, type_selector, active_tab, n_clicks):
    if "tab_alignment" not in active_tab:
        return alignment_functions.alignment_data
    print(species_selected, busco_name_selector, type_selector, active_tab, n_clicks, flush=True)
    if species_selected != None and species_selected !=[] and busco_name_selector != None and busco_name_selector != "None" and busco_name_selector !=[] and type_selector is not None:
        data = alignment_functions.read_in_alignment(species_selected, busco_name_selector, type_selector)
        print("update alignment data", flush=True)
        print(data, flush=True)
        if len(data) > 0:
            #A Match is found -> Alert is left off
            return data, False
        else:
            print("reset to default, None found",flush=True)
            #Alert user that None were found
            print("User alert that no matches are found (Alignment)", flush=True)
            return alignment_functions.alignment_data, True
    else:
        print("Species,Busco and Type must be selected")
        return alignment_functions.alignment_data, False
#----------------------------------------------------------
#----------------------------------------------------------    