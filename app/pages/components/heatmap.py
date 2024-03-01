#This is for all functions pertaining to generating the heatmap from busco data
#----------------------------------------------------------
import os
import pandas as pd
from dash import dcc, html, callback, clientside_callback
from dash.dependencies import ClientsideFunction, Input, Output, State
import plotly.graph_objects as go
import plotly.io as pio
#----------------------------------------------------------
def get_species_list():
    species_list = []
    with open("./data/prot_busco_df.csv") as f:
        species = [row.split(",")[0] for row in f]
        species=species[1:]
    return species
#----------------------------------------------------------
@callback(
    Output(component_id="my_heatmap_graph", component_property="figure"),
    Input(component_id="species_selected", component_property="value"),
)
def get_heatmap_df(species_selected):
    heatmap_df = pd.read_csv('./data/prot_busco_df.csv', index_col=0)

    #filter by user selection
    if species_selected != None and species_selected != "None":
        subset = heatmap_df.loc[species_selected]
    else:
        subset = heatmap_df
    #print(subset)

    fig = go.Figure(data=go.Heatmap(z=subset.values, colorscale=[[0, "darkblue",], [0.33, "purple"], [0.66, "coral"], [1, "gold"]], colorbar=dict(tickmode='array',
                    tickvals=[0, 1, 2, 3], ticktext=["single", "fragmented", "multi", "missing"], title="Busco type"),x=subset.columns, y=subset.index))
    fig.update_xaxes(showticklabels=False)
    fig.update_layout(title="Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
    return fig
#----------------------------------------------------------
heatmap = html.Div(
    [
        html.H5("Heatmap of Species v. Busco Genes"),
        dcc.Graph(id='my_heatmap_graph'),
    ]
)
#----------------------------------------------------------
@callback(
    Output('heatmap', 'config'),
    Input('download-heatmap-button', 'n_clicks'),
    State('my_heatmap_graph', 'figure')
)
def download_heatmap(n_clicks, figure):
    if n_clicks is not None and n_clicks > 0:
        # Save the current figure as a .png image
        pio.write_image(figure, 'heatmap.png')
        print("wrote image")
        # Send the file to the client
        return dcc.send_file('heatmap.png')
#----------------------------------------------------------
    
#----------------------------------------------------------
