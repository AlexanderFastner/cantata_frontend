#This is the app that starts everything else
#----------------------------------------------------------
import os
import dash
import sys
import dash_bootstrap_components as dbc
from flask import Flask
from pages.components.footer import create_footer
#----------------------------------------------------------
FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)
server = Flask(__name__)
app = dash.Dash(
    #app.config.suppress_callback_exceptions = True
    __name__,
    server=server,
    title="Cantata",
    external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME],
    requests_pathname_prefix=os.getenv("SUBDOMAIN", "/"),
    #background_callback_manager=background_callback_manager,
    use_pages=True,
)
app.css.config.serve_locally = True
app.scripts.config.serve_locally = True
app.config.suppress_callback_exceptions = True
#----------------------------------------------------------
app.layout = dbc.Container(
    [
        dbc.NavbarSimple(
            [
                dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
                #TODO change this from Nav Item to dropdown once we can link to individual tools
                for page in dash.page_registry.values()
            ],
            brand="Cantata",
            brand_href="#",
            brand_style={"font-size":"40px"},
            className="navbar navbar-dark bg-dark",
            style={"margin-top":"5px", "border-radius":"5px"},

        ),
        dash.page_container,
        create_footer(),
    ],
    fluid=True,
)

#----------------------------------------------------------
def run_dash_app():
    print("NEW RUN")
    print("---------------------------------------------------")
    # Run the Dash app
    debug = os.getenv("DEBUG", "True") == "True"
    #debug enabled
    #app.run_server(port=8050, debug=True)
    #production
    app.run_server(host='0.0.0.0', port=8050, debug=False)
#----------------------------------------------------------
if __name__ == "__main__":
    run_dash_app()
#----------------------------------------------------------