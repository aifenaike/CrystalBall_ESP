import dash
import dash_bootstrap_components as dbc
import pandas as pd
import layout
import os
import Callbacks 


path = os.path.abspath(os.path.dirname(__file__))


layout = layout.return_layout()

#Initialize Dash app
FONT_AWESOME = "https://use.fontawesome.com/releases/v5.10.2/css/all.css"
# loading 2 stylesheets reduces the flicker when changing themes
external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.themes.BOOTSTRAP, FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,
meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}])
app.title = "Emotion Analytics Dashboard"

app.layout = layout


"""
===============================================================================
Dash App Callbacks 
"""

Callbacks.register_callbacks(app)

if __name__ == '__main__':
    app.run_server(debug=True,use_reloader=False)

   