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
        id="app-footer",
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
                                "github.com/AlexanderFasner",
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
            "font-size": "14px",
            "color": "#666666"
        }
    )
    return footer