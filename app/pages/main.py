#main page containing info and various tools
#----------------------------------------------------------
import collections
import numpy as np
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as ex
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
#----------------------------------------------------------
color_map = {"Complete_BUSCOs": "#785EF0",
                    "Complete_&_single-copy": "#648FFF",
                    "Complete_&_duplicated" : "#DC267F",
                    "Fragmented":"#FE6100",
                    "Missing":"#FFB000"
                    }
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
#heatmap
@callback(
    Output(component_id="busco_heatmap", component_property="figure"),
    Input(component_id="species_selected", component_property="value"),
)
def get_heatmap_df(species_selected):
    #print("Selected species Heatmap:", species_selected)
    heatmap_df = pd.read_csv('./data/prot_busco_df.csv', index_col=0)

    #filter by user selection
    if species_selected != None and species_selected != "None":
        subset = heatmap_df.loc[species_selected]
    else:
        subset = heatmap_df
    #print(subset)

    fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "#648FFF",], [0.33, "#DC267F"], [0.66, "#FE6100"], [1, "#FFB000"]], colorbar=dict(tickmode='array',
                    tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(title="Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
    return fig

#TODO fix/implement this button
@callback(
    Output('heatmap', 'config'),
    Input('download-heatmap-button', 'n_clicks'),
    State('busco_heatmap', 'figure')
)
def download_heatmap(n_clicks, figure):
    if n_clicks is not None and n_clicks > 0:
        # Save the current figure as a .png image
        pio.write_image(figure, 'heatmap.png')
        print("wrote image")
        # Send the file to the client
        return dcc.send_file('heatmap.png')
#----------------------------------------------------------
#TransPi
@callback(
    Output(component_id="TransPi_area", component_property="figure"),
    Input(component_id="species_selected", component_property="value"),
)
def get_TransPi_barplot(species_selected):
    #print("Selected species TransPi:", species_selected)
    TransPi_area_df = pd.read_csv('./data/TransPi.tsv', sep="\t", index_col=0)
    TransPi_area_df = TransPi_area_df.drop(columns=["Complete_BUSCOs", "Total"])

    #filter by user selection
    if species_selected != None and species_selected != "None":
        subset_TransPi = TransPi_area_df.loc[species_selected]
        fig = go.Figure(data=ex.area(subset_TransPi, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                        title="transPi"))
        return fig
    else:
            fig = ""
            return fig

@callback(
    Output('busco_stacked_area_TransPi', 'config'),
    Input('download-stacked-area-TransPi-button', 'n_clicks'),
    State('TransPi_area', 'figure')
)
def download_stacked_area_TransPi(n_clicks, figure):
    if n_clicks is not None and n_clicks > 0:
        # Save the current figure as a .png image
        pio.write_image(figure, 'TransPi_stacked_area.png')
        print("wrote TransPi stacked")
        # Send the file to the client
        return dcc.send_file('TransPi_stacked_area.png')
#----------------------------------------------------------
#Trinity
@callback(
    Output(component_id="Trinity_area", component_property="figure"),
    Input(component_id="species_selected", component_property="value"),
)
def get_Trinity_barplot(species_selected):
    Trinity_area_df = pd.read_csv('./data/Trinity.tsv', sep="\t", index_col=0)
    Trinity_area_df = Trinity_area_df.drop(columns=["Complete_BUSCOs", "Total"])
    #print(Trinity_area_df)

    #filter by user selection
    if species_selected != None and species_selected != "None":
        subset_Trinity = Trinity_area_df.loc[species_selected]
        fig = go.Figure(data=ex.area(subset_Trinity, color_discrete_sequence=["#648FFF", "#DC267F", "#FE6100", "#FFB000"],
                        title="Trinity"))
        return fig
    else:
        fig = ""
        return fig

#TODO fix button
@callback(
    Output('busco_stacked_area_Trinity', 'config'),
    Input('download-stacked-area-Trinity-button', 'n_clicks'),
    State('Trinity_area', 'figure')
)
def download_stacked_area_Trinity(n_clicks, figure):
    if n_clicks is not None and n_clicks > 0:
        # Save the current figure as a .png image
        pio.write_image(figure, 'Trinity_stacked_area.png')
        print("wrote Trinity stacked")
        # Send the file to the client
        return dcc.send_file('Trinity_stacked_area.png')
#----------------------------------------------------------
#Raincloud TransPi



#----------------------------------------------------------
#Raincloud Trinity
@callback(
    Output(component_id="Trinity_Raincloud", component_property="figure"),
    Input(component_id="species_selected", component_property="value"),
)
def get_Trinity_Raincloud(species_selected):
    Trinity_df = pd.read_csv('./data/Trinity.tsv', sep="\t", index_col=0)
    #filter by user selection
    if species_selected != None and species_selected != "None":
        subset_Trinity = Trinity_df.loc[species_selected]

        #print("Subset Trinity: ",subset_Trinity)    
        #data wrangling
        Trinity_column_names = subset_Trinity.columns.to_list()[:-1]
        all_column_values=[]
        for column in Trinity_column_names:
            column_values_Trinity = subset_Trinity[column].values
            all_column_values.append(column_values_Trinity)
        #Construct Plot
        #colors = ["purple","blue","red","orange","gold"]
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
        
        fig.update_layout(title='Violin Plot of BUSCOs Data',
                        xaxis_title='Counts',
                        xaxis=dict(range=[0, None]))
        return fig
    else:
        fig = ""
        return fig

#TODO fix button
@callback(
    Output('busco_Raincloud_Trinity', 'config'),
    Input('download-Raincloud-Trinity-button', 'n_clicks'),
    State('Trinity_Raincloud', 'figure')
)
def download_Raincloud_Trinity(n_clicks, figure):
    if n_clicks is not None and n_clicks > 0:
        # Save the current figure as a .png image
        pio.write_image(figure, 'Trinity_Raincloud.png')
        print("wrote Trinity Raincloud")
        # Send the file to the client
        return dcc.send_file('Trinity_stacked_area.png')

#----------------------------------------------------------
#Raincloud Combined


#---------------------------------------------------------- 