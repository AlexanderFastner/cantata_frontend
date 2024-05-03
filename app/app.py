#This is the main Fask app that starts everything else
#----------------------------------------------------------
import os
port = os.environ.get("PORT", 8050)
import sys
import dash_bootstrap_components as dbc

import dash
from flask import Flask

import pages.components.footer as footer
#----------------------------------------------------------
print("Starting up!", flush=True)
print("---------------------------------------------", flush=True)
sys.stdout.flush()
#----------------------------------------------------------
FONT_AWESOME = (
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css"
)
#----------------------------------------------------------
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
        footer.create_footer(),
    ],
    fluid=True,
)

#----------------------------------------------------------
@server.route('/')
def index():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run_server()
    app.run_server(debug=True, host='0.0.0.0', port=port)
#----------------------------------------------------------