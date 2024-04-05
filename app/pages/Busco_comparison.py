# This holds the page for Busco gene comparison across Species
#----------------------------------------------------------
import dash
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as ex
from pages.components.user_selection import get_species_list, group_options
from pages.components.tabs import plot_selector_tabs
from pages.components.alignment_functions import read_in_alignment
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
from flask import send_file
#----------------------------------------------------------
color_map = {"Complete_BUSCOs": "#785EF0",
                    "Complete_&_single-copy": "#648FFF",
                    "Complete_&_duplicated" : "#DC267F",
                    "Fragmented":"#FE6100",
                    "Missing":"#FFB000"
                    }
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
                                        #TODO Make this a multiselector, with All as default
                                        dcc.Dropdown(
                                            id="group_dropdown",
                                            options=[{'label': category['label'], 'value': category['value']} for category in group_options],
                                            placeholder="Select a Group",
                                        ),
                                        html.Hr(),
                                        html.Button("Update Species", id='update_species_button', n_clicks=0),
                                        html.Hr(),
                                        #TODO Show only those inlcuded in the group/groups selected above
                                        #TODO Start with All, then restrict
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
                    style={"width": "80%"},
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
    #print("update checklist values: ", group_value)
    if group_value == "All":
        #TODO add all options
        updated_options = ["Abeoforma_whisleri"]
    #TODO convert from , seperated string into array of strings
    updated_options = group_value.split(',')
    #print("updated_options: ", updated_options)
    return updated_options
#----------------------------------------------------------
#Heatmaps
#----------------------------------------------------------
#Heatmap selector for which dataset you want.
@callback(
    Output(component_id="busco_heatmap", component_property="children"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="heatmap_selector", component_property="value"),
    Input(component_id="difference_switch", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button", component_property="n_clicks"),
    prevent_initial_call=True
)
def get_heatmap_df(species_selected, heatmap_selector, difference_switch, active_tab, update_species_button):
    if "tab_heatmap" not in active_tab:
        return html.P("Not active")
    fig_array=[]
    #filter by user selection
    if species_selected != None and species_selected != "None" and species_selected !=[] and heatmap_selector is not None and heatmap_selector != "None":
        #check which dataset the user wants to see
        for selected in heatmap_selector:   
            if selected == "Protein":
                fig_array.append("Protein_heatmap")
            elif selected == "Trinity":
                fig_array.append("Trinity_heatmap")
            elif selected == "TransPi":
                fig_array.append("TransPi_heatmap")
    else:
        return None
    
    if len(fig_array) >= 2 and difference_switch:
        fig_array.append("Difference_heatmap")
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
#heatmap difference selector update
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
    for item in children:
        #print(item)
        if "Protein_heatmap" in item.get("props").get("id"):
            Prot_heatmap_df = pd.read_csv('./data/busco5_full_table_Proteome_df_numbers.csv', index_col=0)
            Prot_subset = Prot_heatmap_df.loc[Prot_heatmap_df.index.isin(species_selected)]
        if "Trinity_heatmap" in item.get("props").get("id"):
            Trinity_heatmap_df = pd.read_csv('./data/busco4_full_table_Trinity_df_numbers.csv', index_col=0)
            Trinity_subset = Trinity_heatmap_df.loc[Trinity_heatmap_df.index.isin(species_selected)]
        if "TransPi_heatmap" in item.get("props").get("id"):
            TransPi_heatmap_df = pd.read_csv('./data/busco4_full_table_TransPi_df_numbers.csv', index_col=0)
            TransPi_subset = TransPi_heatmap_df.loc[TransPi_heatmap_df.index.isin(species_selected)]        
        
    #difference between all 3
    diff_df = None
    if Prot_subset is not None and Trinity_subset is not None and TransPi_subset is not None:
        diff1 = pd.DataFrame(np.where(Prot_subset == Trinity_subset, 1, 0), columns=Prot_subset.columns, index=Prot_subset.index)
        diff2 = pd.DataFrame(np.where(Prot_subset == TransPi_subset, 1, 0), columns=Prot_subset.columns, index=Prot_subset.index)
        diff_df = pd.DataFrame(np.where(diff1 == diff2, 1, 0), columns=diff1.columns, index=diff1.index)
        #print("all3", diff_df)
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Difference heatmap"),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig
        
    #difference between 2
    elif Prot_subset is not None and Trinity_subset is not None:
        diff_df = pd.DataFrame(np.where(Prot_subset==Trinity_subset,1,0),columns=Prot_subset.columns, index=Prot_subset.index) 
        #print("Prot Trin", diff_df)
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Difference heatmap"),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig
    elif Trinity_subset is not None and Prot_subset is not None:
        diff_df = pd.DataFrame(np.where(Trinity_subset==TransPi_subset,1,0),columns=Trinity_subset.columns, index=Trinity_subset.index) 
        #print("Trin Trans", diff_df)
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Difference heatmap"),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig
    elif Prot_subset is not None and TransPi_subset is not None:
        diff_df = pd.DataFrame(np.where(Prot_subset==TransPi_subset,1,0),columns=Prot_subset.columns, index=Prot_subset.index) 
        #print("Prot Trans", diff_df)   
        #make difference heatmap
        Difference_fig = go.Figure(data=go.Heatmap(z=diff_df.astype(int).values, colorscale=[[0, "#E52B50"], [1, "#BCBCBC"]], colorbar=dict(tickmode='array',
            tickvals=[0, 1], ticktext=["Different", "Same"], title="Difference heatmap"),x=diff_df.columns, y=diff_df.index))
        Difference_fig.update_xaxes(showticklabels=False)
        Difference_fig.update_layout(title="Difference heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
        return Difference_fig    
    
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
            heatmap_df = pd.read_csv('./data/busco5_full_table_Proteome_df_numbers.csv', index_col=0)
            subset = heatmap_df.loc[heatmap_df.index.isin(species_selected)]
            Protein_fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF"], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
            Protein_fig.update_xaxes(showticklabels=False)
            Protein_fig.update_layout(title="Protein Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
            return Protein_fig
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
            heatmap_df = pd.read_csv('./data/busco4_full_table_Trinity_df_numbers.csv', index_col=0)
            subset = heatmap_df.loc[heatmap_df.index.isin(species_selected)]
            Trinity_fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF"], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
            Trinity_fig.update_xaxes(showticklabels=False)
            Trinity_fig.update_layout(title="Trinity Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
            return Trinity_fig
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
            heatmap_df = pd.read_csv('./data/busco4_full_table_TransPi_df_numbers.csv', index_col=0)
            subset = heatmap_df.loc[heatmap_df.index.isin(species_selected)]
            TransPi_fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF"], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
            TransPi_fig.update_xaxes(showticklabels=False)
            TransPi_fig.update_layout(title="TransPi Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
            return TransPi_fig
#----------------------------------------------------------    
#Stacked Area plots       
#----------------------------------------------------------
#Dynamicly generate Stacked Area plots  
#TODO ask about possible overlay
@callback(
    Output(component_id="Stacked_area", component_property="children"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area_selector", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button", component_property="n_clicks"),
    prevent_initial_call=True
)     
def get_stacked_area(species_selected, Stacked_area_selector, active_tab, update_species_button):
    if "tab_stacked_area" not in active_tab:
        return html.P("Not active (This shouldn't happen)") 
    fig_array=[]
    #filter by user selection
    if species_selected != None and species_selected != "None" and species_selected !=[] and Stacked_area_selector != "None" and Stacked_area_selector is not None:
        #check which dataset the user wants to see
        for selected in Stacked_area_selector:   
            #print("selected", selected)
            if selected == "Protein":
                fig_array.append("Protein_stacked_area")
            elif selected == "Trinity":
                fig_array.append("Trinity_stacked_area")
            elif selected == "TransPi":
                fig_array.append("TransPi_stacked_area")
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
#Protein area
@callback(
    Output(component_id="Protein_stacked_area", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area", component_property="children"),
)
def update_TransPi(species_selected, children):
    for item in children:
        if "Protein_stacked_area" in item.get("props").get("id"):
            if species_selected != None and species_selected != "None" and species_selected !=[]:
                Protein_area_df = pd.read_csv('./data/busco5_short_summary_Proteome.tsv', sep="\t", index_col=0)
                Protein_area_df = Protein_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                subset_Protein = Protein_area_df.loc[Protein_area_df.index.isin(species_selected)]
                fig = go.Figure(data=ex.area(subset_Protein, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                                title="Protein"))
                return fig
            else:
                fig = None
                return fig
#----------------------------------------------------------       
#Trinity area
@callback(
    Output(component_id="Trinity_stacked_area", component_property="figure"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Stacked_area", component_property="children"),
)
def get_Trinity_barplot(species_selected, children):
    #filter by user selection
    for item in children:
        if "Trinity_stacked_area" in item.get("props").get("id"):
            if species_selected != None and species_selected != "None" and species_selected !=[]:
                #print("Trinity", species_selected)
                Trinity_area_df = pd.read_csv('./data/busco4_short_summary_Trinity.tsv', sep="\t", index_col=0)
                Trinity_area_df = Trinity_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                subset_Trinity = Trinity_area_df.loc[Trinity_area_df.index.isin(species_selected)]
                #print(subset_Trinity)
                fig = go.Figure(data=ex.area(subset_Trinity, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                                title="Trinity"))
                return fig
            else:
                fig = None
                return fig

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
def get_TransPi_barplot(species_selected, children):
    #print("species_selected ",species_selected)
    for item in children:
        if "TransPi_stacked_area" in item.get("props").get("id"):
            if species_selected != None and species_selected != "None" and species_selected !=[]:
                TransPi_area_df = pd.read_csv('./data/busco4_short_summary_TransPi.tsv', sep="\t", index_col=0)
                TransPi_area_df = TransPi_area_df.drop(columns=["Complete_BUSCOs", "Total"])
                subset_TransPi = TransPi_area_df.loc[TransPi_area_df.index.isin(species_selected)]
                fig = go.Figure(data=ex.area(subset_TransPi, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                                title="TransPi"))
                return fig
            else:
                fig = None
                return fig

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
#Raincloud selection
#----------------------------------------------------------
#Dynamicly generate Rainclouds
@callback(
    Output(component_id="Rainclouds", component_property="children"),
    State(component_id="species_selected", component_property="value"),
    Input(component_id="Raincloud_selector", component_property="value"),
    Input(component_id="tabs", component_property="active_tab"),
    Input(component_id="update_species_button", component_property="n_clicks"),
    prevent_initial_call=True
)
def get_Rainclouds(species_selected, Raincloud_selector, active_tab, update_species_button):
    if "tab_raincloud" not in active_tab:
        return html.P("Not active")
    fig_array=[]
    #filter by user selection
    #print("raincloud: ", species_selected)
    if species_selected is not None and species_selected != "None" and species_selected !=[] and Raincloud_selector != "None" and Raincloud_selector is not None:
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
            if species_selected != None and species_selected != "None" and species_selected !=[]:
                Protein_df = pd.read_csv('./data/busco5_short_summary_Proteome.tsv', sep="\t", index_col=0)
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
                    fig.add_trace(go.Scatter(x=values, y=c, mode='markers', showlegend=False, marker=dict(color=color_map.get(category))))
                
                fig.update_layout(title='Protein Raincloud Plot of BUSCOs Data',
                                xaxis_title='Counts',
                                xaxis=dict(range=[0, None]))
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
            if species_selected != None and species_selected != "None" and species_selected !=[]:
                TransPi_df = pd.read_csv('./data/busco4_short_summary_TransPi.tsv', sep="\t", index_col=0)
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
                    fig.add_trace(go.Scatter(x=values, y=c, mode='markers', showlegend=False, marker=dict(color=color_map.get(category))))
                
                fig.update_layout(title='TransPi Raincloud Plot of BUSCOs Data',
                                xaxis_title='Counts',
                                xaxis=dict(range=[0, None]))
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
            if species_selected != None and species_selected != "None" and species_selected !=[]:
                Trinity_df = pd.read_csv('./data/busco4_short_summary_Trinity.tsv', sep="\t", index_col=0)
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
                    fig.add_trace(go.Scatter(x=values, y=c, mode='markers', showlegend=False, marker=dict(color=color_map.get(category))))
                
                fig.update_layout(title='Trinity Raincloud Plot of BUSCOs Data',
                                xaxis_title='Counts',
                                xaxis=dict(range=[0, None]))
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
#TODO Raincloud Combined




#---------------------------------------------------------- 
#Alignment
#----------------------------------------------------------
#TODO Add selector
#----------------------------------------------------------
@callback(
    Output(component_id="alignment_viewer", component_property="data"),
    State(component_id="species_selected", component_property="value"),
    State(component_id="busco_name_selector", component_property="value"),
    Input(component_id="type_selector", component_property="value"),
    prevent_initial_call=True
)
def update_align(species_selected, busco_name_selector, type_selector):
    if species_selected != None and species_selected != "None" and species_selected !=[] and busco_name_selector != None and busco_name_selector != "None" and busco_name_selector !=[]:
        data = read_in_alignment(species_selected, busco_name_selector)
        #print("returning data")
        #print(data)
        return data
    else:
        print("Both species and busco must be selected")
        return ""
#----------------------------------------------------------

#----------------------------------------------------------    