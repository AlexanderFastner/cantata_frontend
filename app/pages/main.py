#main page containing info and various tools
#----------------------------------------------------------
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
#----------------------------------------------------------
dash.register_page(__name__, path="/")
#----------------------------------------------------------
#Overview layout
#row1
    #col1
        #row2 intro
        #row3 new additions
        #row4 our data
    #col2
        #row5 examples
#----------------------------------------------------------

layout = html.Div([
    #TODO add logo
    #TODO add styling and background colors
    dbc.Row(
        [
        dbc.Col(
            [
            dbc.Row(
                [
                dbc.Card(
                    [
                    dbc.CardHeader(html.H2("Community bAsed Non-bilaTeriAn Transcriptome Archive")),
                    dbc.CardBody(
                        [
                        #dbc.CardLink("Cantata", href="https://en.wikipedia.org/wiki/Cantata"),
                        dcc.Markdown(
                            '''
                            A cantata is a vocal composition with an instrumental accompaniment, typically in several movements, often involving a choir [Cantata](https://en.wikipedia.org/wiki/Cantata).
                            --- 

                            **CANTATA** is also a **C**ommunity b**A**sed **N**on-bila**T**eri**A**n **T**ranscriptome **A**rchive. The aim of this project is to provide an archive of non-bilaterian
                            transcriptomic resources assembled and annotated in a standardized manner. You can help further mantaining this archive by simply pushing
                            text files with SRA read `ftp` addresses of the reads to be assembled (see below). The assembly and annotation will be done using computational
                            resources of the Chair of Paläontology and Geobiology of the Dept. of Geo- and Environmental Sciences of the LMU München and made
                            available to the community as a `DOI` minted CANTATA release.
                                    
                            '''
                        )  
                        ],
                    ),
                    ]
                ),
                ],
                className="row2"
            ),
            dbc.Row(
                [
                dbc.Card(
                    [
                    dbc.CardBody(
                        [
                        dbc.CardHeader(html.H4("Suggesting new additions")),
                        dcc.Markdown(
                            '''
                            If you know of a non-bilaterian taxon for which transcriptomic resources are available and is not included in our latest release, you can help us uploading (pushing if you cloned the repository) a plain text file named after the taxon of interest, (e.g., Ephydatia_fluviatilis.txt) with the ftp addresses of the files to be assembled in the `requests` folder available in the repository. For instance, if you want to add E. fluviatilis, the text file `Ephydatia_fluviatilis.txt` would look like:

                            >
                            >  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR297/004/SRR2971104/SRR2971104_1.fastq.gz
                            >  ftp://ftp.sra.ebi.ac.uk/vol1/fastq/SRR297/004/SRR2971104/SRR2971104_2.fastq.gz                            
                            >

                            The file consists of only two lines with the European Nucleotide Archive ftp adresses of the reads to be assembled. If more that one library (assuming pair-end reads this is two lines in the text file) is available for the taxon, you can add several lines. We will download all the files and concatenate them before assembly. Please be sure that:
                            the reads are of the same length in all the files to concatenate.
                            you only include pair-end read files in the file.
                            We cannot warranty the taxon is going to be included in the database immediately upon entering the todo folder area. Running the pipeline costs CPU time and other resources. Therefore, the inclusion of new transcriptomes will be done whenever free resources are available. We hope as soon as the number of transcriptomes in the todo folder drops, we will be able to process new suggestions faster. 

                            '''
                        ),
                        ]
                    )
                    ]
                ),
                ],
                className="row3"
            ),
            dbc.Row(
                [
                dbc.Card(
                    dbc.CardBody(
                        [
                        dbc.CardHeader(html.H4("Our Data")),
                        dcc.Markdown('''
                            Overview of available species\n
                            Add Overview Tree Here!
                            link to figshare\n
                            '''),
                        ]
                    )
                )
                ],
                className="row4"
            ),

            ],
            width={"size": "7"},
            className="col1"
        ),
        dbc.Col(
            [
            dbc.Card(
                dbc.CardBody(
                    [
                    #TODO auto navigate user to that tool with links
                        ### [Heatmap of buscos](/Busco)
                        ### [Stacked Area plots](/Busco)  
                        ### [Raincloud plots](/Busco) 
                        ### [Alignment Comparison](/Busco)  
                       
                    dcc.Markdown(
                        '''
                        ## Ways to Analyze Buscos:    
                        ---
                        ### Heatmap of buscos  
                        ![heatmap example](/assets/heatmap_example.png#example)  

                        ### Stacked Area plots  
                        ![stacked area example](/assets/stacked_area_example.png#example)  
                         
                        ### Raincloud plots  
                        ![raincloud example](/assets/raincloud_example.png#example)  

                        ### Alignment Comparison  
                        ![alignment example](/assets/alignment_example.png#example)  
                        
                        '''
                    ),
                    ],
                )
            )
            ],
            width={"size": "5", "offset": "0"},
            className="col2"        
            ),
        ],
        className="row1"
    ),
])