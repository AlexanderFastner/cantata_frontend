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
#Startup instructions

#conda activate cantata_frontend    
#heroku login
#heroku container:login

#in local terminal in desired dir with dockerfile

#heroku container:push web
#heroku container:release web
#----------------------------------------------------------
print("Starting up!")
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
#The layout contains the general structure of the app
#NavbarSimple is navigation bar at the top
#the dash.pageregistry contains the various pages I built
    #That structure is in tabs.py
#The footer is seperate from the otehr pages as it is added to everything
app.layout = dash.html.Div(
    [
        dash.html.Div(
            [
                dbc.NavbarSimple(
                    [
                        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
                        for page in dash.page_registry.values()
                    ],
                    brand="Cantata",
                    brand_href="#",
                    fluid=True,
                    brand_style={"font-size":"40px"},
                    className="navbar navbar-dark bg-dark",
                    #style={"border-radius":"5px"},
                ),
                dash.html.Div(
                    dash.page_container,
                    id="page-content",
                    style={'flex': '1', 'overflow': 'auto'}
                ),
            ], id="content-wrapper", style={'display': 'flex', 'flexDirection': 'column', 'minHeight': '100vh'}),
            footer.create_footer(),
    ], 
    style={'position': 'relative', 'minHeight': '100vh'},
    id='Outer-Container'
)

print("layout made")
print("---------------------------------------------", flush=True)


#----------------------------------------------------------
@server.route('/')
def index():
    return 'Hello, World!'

if __name__ == "__main__":
    app.run_server()
    app.run_server(debug=True, host='0.0.0.0', port=port)
#----------------------------------------------------------
#TODO
#fix footer to bottom --done
#fix scrollbar sizing --done
#seperate scrollbar with individuals from group --done
#fix None group selection, rename Clear Selection --todo
#stcked area comparison options move to under other selection --todo
    #only appear when that checklist option is selected --todo
#remove the rounding on header corners --done
#add tooltips --todo


#User upload data
    #add button for this
    #how to select data?


#----------------------------------------------------------
