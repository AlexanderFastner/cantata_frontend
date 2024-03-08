#main page containing info and various tools
#----------------------------------------------------------
import collections
import pandas as pd
import dash
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.express as ex
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
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
    print("Selected species Heatmap:", species_selected)
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
    print("Selected species TransPi:", species_selected)
    TransPi_area_df = pd.read_csv('./data/TransPi.tsv', sep="\t", index_col=0)
    TransPi_area_df = TransPi_area_df.drop(columns=["Complete_BUSCOs", "Total"])
    #print(TransPi_area_df.head)    

    #filter by user selection
    if species_selected != None and species_selected != "None":
        subset_TransPi = TransPi_area_df.loc[species_selected]
    else:
        subset_TransPi = TransPi_area_df

    fig = go.Figure(data=ex.area(subset_TransPi))
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
        print("wrote TransPi image")
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
    else:
        subset_Trinity = Trinity_area_df

    fig = go.Figure(data=ex.area(subset_Trinity))
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
        print("wrote Trinity image")
        # Send the file to the client
        return dcc.send_file('Trinity_stacked_area.png')
#----------------------------------------------------------

#----------------------------------------------------------
