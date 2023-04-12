import os
import pathlib

import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
from utils import *
import Callbacks

import pandas as pd

path = os.path.abspath(os.path.dirname(__file__))

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Predictive Maintenance Analytics Dashboard"
server = app.server
app.config["suppress_callback_exceptions"] = True

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(app),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                build_tabs(),
                # Main app
                html.Div(id="app-content"),
            ],
        ),
        dcc.Store(id="value-setter-store", data=init_value_setter_store()),
        dcc.Store(id="n-interval-stage", data=50),
        generate_modal(),
    ],
)

Callbacks.register_callbacks(app)

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8060, use_reloader=True)
