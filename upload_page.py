import os
import pathlib

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)
app.title = "Predictive Maintenance Analytics Dashboard"
server = app.server
app.config["suppress_callback_exceptions"] = True

APP_PATH = str(pathlib.Path(__file__).parent.resolve())
df = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "composite.csv")))

params = list(df)
max_length = len(df)

suffix_row = "_row"
suffix_button_id = "_button"
suffix_sparkline_graph = "_sparkline_graph"
suffix_count = "_count"
suffix_ooc_n = "_OOC_number"
suffix_ooc_g = "_OOC_graph"
suffix_indicator = "_indicator"


def build_banner():
    return html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Predictive Maintenance Analytics Dashboard"),
                    html.H6("Electrical Submersible Pump Control Exception Reporting Platform"),
                ],
            ),
            html.Div(
                id="banner-logo",
                children=[
                    html.A(
                        html.Button(children="Dashboard"),
                        href="https://plotly.com/get-demo/",
                    ),
                    html.A(
                        html.Button(children="Prediction (ML)"),
                        href="https://plotly.com/get-demo/",
                    ),
                    html.Button(
                        id="learn-more-button", children="LEARN MORE", n_clicks=0
                    ),
                    html.A(
                        html.Img(id="logo", src=app.get_asset_url("dash-logo-new.png")),
                        href="https://plotly.com/dash/",
                    ),
                ],
            ),
        ],
    )



def build_tabs():
    return html.Div(
        id="tabs",
        className="tabs",
        children=[
            dcc.Tabs(
                id="app-tabs",
                value="tab1",
                className="custom-tabs",
                children=[
                    dcc.Tab(
                        id="Specs-tab",
                        label="Data Upload and Model Specification",
                        value="tab1",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                    dcc.Tab(
                        id="Control-chart-tab",
                        label="Predictive Analytics Dashboard",
                        value="tab2",
                        className="custom-tab",
                        selected_className="custom-tab--selected",
                    ),
                ],
            )
        ],
    )


##Initialize Upload data
app_upload = html.Div([
                html.Div(id="set_upload_message",
                    children = html.Label(html.H6(html.Strong("Upload Time-series ESP Data"), className="mt-2"),style={"margin-left": "55px"}),
                ),
                    dcc.Upload(['Drag and Drop or ', html.A('Select a File')], 
                    style={
                        'width': '30%',
                        'height': '60px',
                        'lineHeight': '60px',
                        'borderWidth': '1px',
                        'borderStyle': 'dashed',
                        'borderRadius': '5px',
                        'margin-top': '25px',
                        'margin-bottom': '45px',
                        'margin-left': '55px',
                        'textAlign': 'center'},id = 'upload_difference_table'),
                ])

def build_tab_1():
    return [
                #short note
                html.Div(html.P(children=[html.Strong("In order to perform predictive diagnosis of Electrical Submersible Pumps (ESPs), several types of operational data are required."),html.Br(),
                            html.Strong("This includes data from sensors such as vibration sensors, temperature sensors, pressure sensors, and flow sensors."),html.Br(),
                            html.Strong("This data can be used to monitor the condition of the pump and detect any abnormalities or deviations from normal operating conditions."),html.Br(),html.Br(),
                            html.Strong("Here you are required to upload a csv or excel file containing operational data such as discharge_pressure, intake_pressure, vibration, frequency, motor_temperature and current."),html.Br()],
                            style={"margin-left": "55px"})),
                html.Br(),html.Br(),

                #Upload button
                html.Div(app_upload),

                # Adding Dropdown for selecting Sections.
                html.Div(id='select_model_type',
                    children= [
                        html.Label(html.H6(html.Strong("Select a Model Architecture"), className="mt-2"),style={"margin-left": "55px"}),
                        dcc.Dropdown(
                        id="model_id",
                        options=[
                            {"label": "Random Forests", "value": "0"},
                            {"label": "Gradient Boosting Classifier", "value": "1"},
                            {"label": "Anomaly detection", "value": "2"},
                            ],
                        searchable=False,
                        style={ "color": "Navy", 'margin-top': '25px','height': '60px', 'align-items': 'center',
                        'margin-bottom': '45px','margin-left': '27px','width': '50%',
                         'borderRadius': '5px',"textAlign": "center",'justify-content': 'center'},
                        value="0",
                        )]
                    ),
                dbc.Button("Analyze Data",id="submit-button",color = "primary",outline=True, className="mr-2", n_clicks=0,style={"margin-left": "195px",}),
    ]
#########

########Layout

app.layout = html.Div(
    id="big-app-container",
    children=[
        build_banner(),
        dcc.Interval(
            id="interval-component",
            interval=2 * 1000,  # in milliseconds
            n_intervals=50,  # start at batch 50
            disabled=True,
        ),
        html.Div(
            id="app-container",
            children=[
                #Tab Header
                build_tabs(),
                html.Br(),html.Br(),
                # Main app
                html.Div(id="app-content"),          
            ],
        ),
    ],
)



##callbacks

@app.callback(
    Output("app-content", "children"),
    [Input("app-tabs", "value")],
)
def render_tab_content(tab_switch):
    if tab_switch == "tab1":
        return build_tab_1()
    return (
        html.Div(
            id="status-container",
            children=html.P("Let get this"),
                ),
    )


# # Update interval
# @app.callback(
#     Output("n-interval-stage", "data"),
#     [Input("app-tabs", "value")],
#     [
#         State("interval-component", "n_intervals"),
#         State("interval-component", "disabled"),
#         State("n-interval-stage", "data"),
#     ],
# )
# def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
#     if disabled:
#         return cur_interval

#     if tab_switch == "tab1":
#         return cur_interval
#     return cur_stage


# # Callbacks for stopping interval update
# @app.callback(
#     [Output("interval-component", "disabled"), Output("stop-button", "buttonText")],
#     [Input("stop-button", "n_clicks")],
#     [State("interval-component", "disabled")],
# )
# def stop_production(n_clicks, current):
#     if n_clicks == 0:
#         return True, "start"
#     return not current, "stop" if current else "start"


######

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, port=8040, use_reloader=True)