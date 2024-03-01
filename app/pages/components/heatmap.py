#This is for all functions pertaining to generating the heatmap from busco data
#----------------------------------------------------------
import os
import pandas as pd
from dash import dcc, html
import plotly.graph_objects as go
#----------------------------------------------------------
def get_species_list():
    species_list = []
    with open("./data/prot_busco_df.csv") as f:
        species = [row.split(",")[0] for row in f]
        species=species[1:]
    return species
#----------------------------------------------------------
def get_heatmap_df():
    heatmap_df = pd.read_csv('./data/prot_busco_df.csv')

    #TODO filter by user selection
    fig = go.Figure(data=go.Heatmap(z=heatmap_df.values, colorscale='turbo', colorbar=dict(tickmode='array',
                    tickvals=[0, 1, 2], ticktext=["0", "1", "2"], title="Busco type"),x=heatmap_df.columns, y=heatmap_df.index))

    fig.update_layout(title="Busco Heatmap", xaxis_title="Busco Genes", yaxis_title="Species")
    #print(fig)
    return fig
#----------------------------------------------------------
heatmap = html.Div(
    [
        html.H5("Heatmap of Species v. Busco Genes"),
        dcc.Graph(figure=get_heatmap_df(), id='my_heatmap_graph'),
    ]
)
#----------------------------------------------------------
