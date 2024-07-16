#footer component
#----------------------------------------------------------
from dash import html
#----------------------------------------------------------
#return a basic footer
def create_footer():
    """
    Generates a basic footer for the Dash app with a link to the GitHub profile.
    """
    footer = html.Footer(
        id="footer",
        children=[
            html.Div(
                className="footer-content",
                children=[
                    html.Div(
                        children=[
                            "!PLACEHOLDER! © 2023 Cantata Transcriptomic Database. All rights reserved."
                        ]
                    ),
                    html.Div(
                        children=[
                            "Powered by Dash, a product of Plotly."
                        ]
                    ),
                    html.Div(
                        children=[
                            "Visit my GitHub: ",
                            html.A(
                                "github.com/AlexanderFastner",
                                href="https://github.com/AlexanderFastner",
                                target="_blank",
                                style={
                                    "color": "#007bff",
                                    "text-decoration": "none"
                                }
                            )
                        ]
                    )
                ]
            )
        ],
        style={
            "background-color": "#f5f5f5",
            "padding": "20px",
            "text-align": "center",
            'position': 'absolute',
            "font-size": "14px",
            "color": "#666666",
            'bottom': '0',
            'width': '100%',
            'marginTop': 'auto',
        }
    )

    return footer