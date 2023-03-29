import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np
import utils
import dash_tables
import os


path = os.path.abspath(os.path.dirname(__file__))
# difference_df = pd.read_excel(path + "/data/diff.xlsx")
# emoji_count = pd.read_excel(path+ "/data/emoji.xlsx")
# emotion_score = pd.read_excel(path + "/data/emotion.xlsx")

all_options = {
    "Not Specified": ["Not Specified"],
    "Watch Other": [
        "Caucasian or White",
        "Asian or Pacific Islander",
        "Hispanic or Latino",
        "African American or Black",
    ],
    "Watch Gender": ["Female", "Male"],
    "Watch Age Range": ["18-24", "25-29", "30-34", "35-39"],
}

mini_options = {
    "Emoji_Data": ["Cupcake", "Truly"],
    "Emotion_Data": ["Cupcake", "Truly"],
    "Difference_Data": ["Both Brands"],
}
names = list(all_options.keys())
nestedOptions = all_options[names[0]]
mini_names = list(mini_options.keys())
mini_nestedOptions = mini_options[mini_names[0]]

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "20%",
    "padding": "20px 10px",
    "background-color": "#f8f9fa",
    "minWidth": 250,
}


"""
===============================================================
sidebar
"""

Pump_type_card = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label(
                    html.H6(
                        "Enter the Number of Pumps the data you intend to Analyze has (Standard vs What's New included)",
                        className="mt-2",
                    ),
                    size="md",
                ),
                dbc.Input(id="value_input", value=10, type="number", min=1, max=15),
                dbc.Label(html.H4("Pump Type", className="mt-2")),
                # Adding Dropdown for selecting Sections.
                dcc.Dropdown(
                    id="pump_id",
                    options=[
                        {"label": "Pump 859", "value": "0"},
                        {"label": "Pump 851", "value": "1"},
                        {"label": "Pump 451", "value": "2"},
                        {"label": "Pump 680", "value": "3"},
                    ],
                    searchable=False,
                    style={"textAlign": "center", "color": "Navy"},
                    value="0",
                ),
            ]
        ),
    ],
    className="px-2 mb-2",
    style={"minWidth": 200},
)

Parameters_card = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label(html.H4("Parameters", className="mt-2")),
                # Adding Dropdown for selecting Sections.
                dcc.Dropdown(
                    id="par_id",
                    options=[
                        {"label": "Current", "value": "0"},
                        {"label": "Pres Discharge", "value": "1"},
                        {"label": "Frequency", "value": "2"},
                        {"label": "Pres Intake", "value": "3"},
                        {"label": "Temp Intake", "value": "4"},
                        {"label": "Temp Motor Pump", "value": "5"},
                        {"label": "Vibration", "value": "6"},
                    ],
                    searchable=False,
                    style={"textAlign": "center", "color": "Navy"},
                    value="0",
                ),
            ]
        ),
    ],
    className="px-2 mb-2",
    style={"minWidth": 200},
)

Date_picker_card = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label(html.H4("Date Picker", className="mt-2")),
                dcc.DatePickerRange(
                    id="date_picker",
                    min_date_allowed=utils.min_date,
                    max_date_allowed=utils.max_date,
                    initial_visible_month=utils.max_date,
                    start_date=utils.min_date,
                    end_date=utils.max_date,
                    display_format="MMM Do, YY",
                    style={"textAlign": "center", "color": "Navy"},
                ),
            ]
        ),
    ],
    className="px-2 mb-2",
    style={"minWidth": 200},
)

Visualization_card = html.Div(
    [
        dbc.FormGroup(
            [
                dbc.Label(html.H4("Visualization Options", className="mt-2")),
                dcc.RadioItems(
                    id="type_id",
                    options=[
                        {"label": "Line Plots", "value": 1},
                        {"label": "Scatter Plots", "value": 2},
                    ],
                    labelStyle={"display": "block", "color": "Navy"},
                    value=1,
                ),
            ]
        ),
    ],
    className="px-2 mb-2",
    style={"minWidth": 200},
)

# Adding Sidebar for dashboard navigation elements
sidebar = dbc.Card(
    [
        dbc.CardHeader(html.H2("Parameters", className="bg-primary text-white p-2")),
        dbc.CardBody(
            [
                Pump_type_card,
                Parameters_card,
                Date_picker_card,
                Visualization_card,
            ],
        ),
    ],
    style={"minWidth": 250, "height": "100vh"},
)


"""
===============================================================================
Dash App Content 
"""


# initialize table tab
app_table = html.Div(
    [
        html.Div(id="legend_id", style={"float": "right"}),
        dash_table.DataTable(
            id="Data",
            page_size=10,
            editable=True,
            cell_selectable=True,
            filter_action="native",
            sort_action="native",
            style_table={"overflowX": "auto"},
            style_data_conditional=[
                {
                    "if": {"state": "active"},
                    "border": "1px solid var(--primary)",
                    "opacity": 0.75,
                },
                {
                    "if": {"state": "selected"},
                    "border": "1px solid",
                    "opacity": 0.75,
                },
            ],
        ),
        dcc.Store(id="stored-diff"),
        dcc.Store(id="stored-emoji"),
        dcc.Store(id="stored-emotion"),
    ]
)

# initialize graph tab
app_graphs = html.Div(
    [
        dcc.Markdown(
            id="line_chart_title",
            className="text-center mb-0 d-inline-block",
        ),
        dcc.Graph(id="graph_id"),
    ]
)

##Initialize Upload data
app_upload = html.Div(
    [
        dcc.Markdown(
            id="upload_data",
            className="text-center mb-0 d-inline-block",
        ),
        html.Div(
            [
                html.P("Upload Difference Data", className="pt-2"),
                dcc.Upload(
                    ["Drag and Drop or ", html.A("Select a File")],
                    style={
                        "width": "65%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                    },
                    id="upload_difference_table",
                ),
                html.Hr(),
                html.P("Upload Emoji Data", className="pt-2"),
                dcc.Upload(
                    ["Drag and Drop or ", html.A("Select a File")],
                    style={
                        "width": "65%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                    },
                    id="upload_emoji_data",
                ),
                html.Hr(),
                html.P("Upload Emotion Data", className="pt-2"),
                dcc.Upload(
                    html.Div(["Drag and Drop or ", html.A("Select a File")]),
                    style={
                        "width": "65%",
                        "height": "60px",
                        "lineHeight": "60px",
                        "borderWidth": "1px",
                        "borderStyle": "dashed",
                        "borderRadius": "5px",
                        "textAlign": "center",
                    },
                    id="upload_emotion_data",
                    multiple=False,
                ),
                html.Hr(),
                dbc.Button(
                    "Analyze Data",
                    id="submit-button",
                    color="primary",
                    outline=True,
                    className="mr-2",
                    n_clicks=0,
                ),
            ]
        ),
        html.P(id="diff_placeholder"),
        html.P(id="emoji_placeholder"),
        html.P(id="emotion_placeholder"),
    ]
)

layout_app_controls = dbc.Card(
    [
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Data"),
                            # Adding Dropdown for selecting Sections.
                            dcc.Dropdown(
                                id="data_id",
                                options=[
                                    {"label": name, "value": name}
                                    for name in mini_names
                                ],
                                value=list(mini_options.keys())[0],
                                searchable=False,
                                style={"textAlign": "center"},
                            ),
                        ]
                    )
                ),
                dbc.Col(
                    dbc.FormGroup(
                        [
                            dbc.Label("Select Brand"),
                            # Adding Dropdown for selecting Sections.
                            dcc.Dropdown(id="brand_id", searchable=False),
                        ]
                    )
                ),
            ]
        ),
    ],
    className="mr-4 ml-4 px-2",
)


app_tabs = html.Div(
    [
        dbc.Tabs(
            [
                dbc.Tab(
                    html.Div(
                        [
                            html.P(
                                "Upload Data for Emotion Analytics.The Uploaded Data should include data for feelings, emoji and differences.",
                                className="pt-2",
                            ),
                            app_upload,
                        ]
                    ),
                    label="Uploads",
                    style={"padding": "10px"},
                ),
                dbc.Tab(
                    app_graphs,
                    label="Graphs",
                    style={"padding": "10px"},
                ),
                dbc.Tab(
                    html.Div(
                        [
                            html.P(
                                "Data table for Emotion Analytics.",
                                className="pt-2",
                            ),
                            app_table,
                        ]
                    ),
                    label="Data Table",
                    style={"padding": "10px"},
                ),
            ]
        )
    ],
    className="my-4",
)

layout_app = dbc.Card(
    [
        html.H2("ESP Analytics Dash App", className="bg-primary text-white p-2"),
        dbc.Row(dbc.Col(app_tabs, className="mx-4")),
        layout_app_controls,
    ],
    style={"height": "100vh"},
    className="mx-1 shadow pb-4",
    id="layout_app_container",
)


"""
===============================================================================
Layout
"""


def return_layout():
    layout = dbc.Container(
        [
            utils.header,
            dbc.Row(
                [
                    dbc.Col(sidebar, width=3, md=4),
                    dbc.Col(
                        layout_app,
                        width=9,
                        md=8,
                        sm=12,
                    ),
                ],
                id="layout",
            ),
            html.Div(id="blank_output2"),
        ],
        fluid=True,
        className="dbc_both",
    )
    return layout
