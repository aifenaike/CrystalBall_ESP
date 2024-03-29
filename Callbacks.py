import os
import pathlib
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table
import plotly.graph_objs as go
import dash_daq as daq
import dash_bootstrap_components as dbc
import pandas as pd
from utils import *
import dash

path = os.path.abspath(os.path.dirname(__file__))
data_ = pd.read_csv(os.path.join(APP_PATH, os.path.join("data", "composite_time.csv")))
def register_callbacks(app):
    @app.callback(
    [Output("app-content", "children"), Output("interval-component", "n_intervals")],
    [Input("app-tabs", "value")],
    [State("n-interval-stage", "data")],
    )
    def render_tab_content(tab_switch, stopped_interval):
        if tab_switch == "tab1":
            return build_tab_1(), stopped_interval
        elif tab_switch == "tab3":
            return build_tab_upload(),stopped_interval
        return (
            html.Div(
                id="status-container",
                children=[
                    build_quick_stats_panel(),
                    html.Div(
                        id="graphs-container",
                        children=[build_top_panel(stopped_interval), build_chart_panel()],
                    ),
                ],
            ),
            stopped_interval,
        )


    # Update interval
    @app.callback(
        Output("n-interval-stage", "data"),
        [Input("app-tabs", "value")],
        [
            State("interval-component", "n_intervals"),
            State("interval-component", "disabled"),
            State("n-interval-stage", "data"),
        ],
    )
    def update_interval_state(tab_switch, cur_interval, disabled, cur_stage):
        if disabled:
            return cur_interval

        if tab_switch == "tab1":
            return cur_interval
        return cur_stage


    # Callbacks for stopping interval update
    @app.callback(
        [Output("interval-component", "disabled"), Output("stop-button", "buttonText")],
        [Input("stop-button", "n_clicks")],
        [State("interval-component", "disabled")],
    )
    def stop_production(n_clicks, current):
        if n_clicks == 0:
            return True, "start"
        return not current, "stop" if current else "start"


    # ======= Callbacks for modal popup =======
    @app.callback(
        Output("markdown", "style"),
        [Input("learn-more-button", "n_clicks"), Input("markdown_close", "n_clicks")],
    )
    def update_click_output(button_click, close_click):
        ctx = dash.callback_context

        if ctx.triggered:
            prop_id = ctx.triggered[0]["prop_id"].split(".")[0]
            if prop_id == "learn-more-button":
                return {"display": "block"}

        return {"display": "none"}


    # ======= update progress gauge =========
    @app.callback(
        output=Output("progress-gauge", "value"),
        inputs=[Input("interval-component", "n_intervals")],
    )
    def update_gauge(interval):
        if interval < max_length:
            total_count = interval
        else:
            total_count = max_length

        return int(total_count)


    # ===== Callbacks to update values based on store data and dropdown selection =====
    @app.callback(
        output=[
            Output("value-setter-panel", "children"),
            Output("ud_usl_input", "value"),
            Output("ud_lsl_input", "value"),
            Output("ud_ucl_input", "value"),
            Output("ud_lcl_input", "value"),
        ],
        inputs=[Input("metric-select-dropdown", "value")],
        state=[State("value-setter-store", "data")],
    )
    def build_value_setter_panel(dd_select, state_value):
        return (
            [
                build_value_setter_line(
                    "value-setter-panel-header",
                    "Specs",
                    "Historical Value",
                    "Set new value",
                ),
                build_value_setter_line(
                    "value-setter-panel-usl",
                    "Upper Specification limit",
                    state_dict[dd_select]["usl"],
                    ud_usl_input,
                ),
                build_value_setter_line(
                    "value-setter-panel-lsl",
                    "Lower Specification limit",
                    state_dict[dd_select]["lsl"],
                    ud_lsl_input,
                ),
                build_value_setter_line(
                    "value-setter-panel-ucl",
                    "Upper Control limit",
                    state_dict[dd_select]["ucl"],
                    ud_ucl_input,
                ),
                build_value_setter_line(
                    "value-setter-panel-lcl",
                    "Lower Control limit",
                    state_dict[dd_select]["lcl"],
                    ud_lcl_input,
                ),
            ],
            state_value[dd_select]["usl"],
            state_value[dd_select]["lsl"],
            state_value[dd_select]["ucl"],
            state_value[dd_select]["lcl"],
        )


    # ====== Callbacks to update stored data via click =====
    @app.callback(
        output=Output("value-setter-store", "data"),
        inputs=[Input("value-setter-set-btn", "n_clicks")],
        state=[
            State("metric-select-dropdown", "value"),
            State("value-setter-store", "data"),
            State("ud_usl_input", "value"),
            State("ud_lsl_input", "value"),
            State("ud_ucl_input", "value"),
            State("ud_lcl_input", "value"),
        ],
    )
    def set_value_setter_store(set_btn, param, data, usl, lsl, ucl, lcl):
        if set_btn is None:
            return data
        else:
            data[param]["usl"] = usl
            data[param]["lsl"] = lsl
            data[param]["ucl"] = ucl
            data[param]["lcl"] = lcl

            # Recalculate ooc in case of param updates
            data[param]["ooc"] = populate_ooc(df[param], ucl, lcl)
            return data


    @app.callback(
        output=Output("value-setter-view-output", "children"),
        inputs=[
            Input("value-setter-view-btn", "n_clicks"),
            Input("metric-select-dropdown", "value"),
            Input("value-setter-store", "data"),
        ],
    )
    def show_current_specs(n_clicks, dd_select, store_data):
        if n_clicks > 0:
            curr_col_data = store_data[dd_select]
            new_df_dict = {
                "Specs": [
                    "Upper Specification Limit",
                    "Lower Specification Limit",
                    "Upper Control Limit",
                    "Lower Control Limit",
                ],
                "Current Setup": [
                    curr_col_data["usl"],
                    curr_col_data["lsl"],
                    curr_col_data["ucl"],
                    curr_col_data["lcl"],
                ],
            }
            new_df = pd.DataFrame.from_dict(new_df_dict)
            return dash_table.DataTable(
                style_header={"fontWeight": "bold", "color": "inherit"},
                style_as_list_view=True,
                fill_width=True,
                style_cell_conditional=[
                    {"if": {"column_id": "Specs"}, "textAlign": "left"}
                ],
                style_cell={
                    "backgroundColor": "#1e2130",
                    "fontFamily": "Open Sans",
                    "padding": "0 2rem",
                    "color": "darkgray",
                    "border": "none",
                },
                css=[
                    {"selector": "tr:hover td", "rule": "color: #91dfd2 !important;"},
                    {"selector": "td", "rule": "border: none !important;"},
                    {
                        "selector": ".dash-cell.focused",
                        "rule": "background-color: #1e2130 !important;",
                    },
                    {"selector": "table", "rule": "--accent: #1e2130;"},
                    {"selector": "tr", "rule": "background-color: transparent"},
                ],
                data=new_df.to_dict("records"),
                columns=[{"id": c, "name": c} for c in ["Specs", "Current Setup"]],
            )


    # decorator for list of output
    def create_callback(param):
        def callback(interval, stored_data):
            count, ooc_n, ooc_g_value, indicator = update_count(
                interval, param, stored_data
            )
            spark_line_data = update_sparkline(interval, param)
            return count, spark_line_data, ooc_n, ooc_g_value, indicator

        return callback


    for param in params[1:]:
        update_param_row_function = create_callback(param)
        app.callback(
            output=[
                Output(param + suffix_count, "children"),
                Output(param + suffix_sparkline_graph, "extendData"),
                Output(param + suffix_ooc_n, "children"),
                Output(param + suffix_ooc_g, "value"),
                Output(param + suffix_indicator, "color"),
            ],
            inputs=[Input("interval-component", "n_intervals")],
            state=[State("value-setter-store", "data")],
        )(update_param_row_function)


    #  ======= button to choose/update figure based on click ============
    @app.callback(
        output=Output("control-chart-live", "figure"),
        inputs=[
            Input("interval-component", "n_intervals"),
            Input(params[1] + suffix_button_id, "n_clicks"),
            Input(params[2] + suffix_button_id, "n_clicks"),
            Input(params[3] + suffix_button_id, "n_clicks"),
            Input(params[4] + suffix_button_id, "n_clicks"),
            Input(params[5] + suffix_button_id, "n_clicks"),
            Input(params[6] + suffix_button_id, "n_clicks"),
            Input(params[7] + suffix_button_id, "n_clicks"),
        ],
        state=[State("value-setter-store", "data"), State("control-chart-live", "figure")],
    )
    def update_control_chart(interval, n1, n2, n3, n4, n5, n6, n7, data, cur_fig):
        # Find which one has been triggered
        ctx = dash.callback_context

        if not ctx.triggered:
            return generate_graph(interval, data, params[1])

        if ctx.triggered:
            # Get most recently triggered id and prop_type
            splitted = ctx.triggered[0]["prop_id"].split(".")
            prop_id = splitted[0]
            prop_type = splitted[1]

            if prop_type == "n_clicks":
                curr_id = cur_fig["data"][0]["name"]
                prop_id = prop_id[:-7]
                if curr_id == prop_id:
                    return generate_graph(interval, data, curr_id)
                else:
                    return generate_graph(interval, data, prop_id)

            if prop_type == "n_intervals" and cur_fig is not None:
                curr_id = cur_fig["data"][0]["name"]
                return generate_graph(interval, data, curr_id)


    # Update piechart
    @app.callback(
        output=Output("piechart", "figure"),
        inputs=[Input("interval-component", "n_intervals")],
        state=[State("value-setter-store", "data")],
    )
    def update_piechart(interval, stored_data):
        if interval == 0:
            return {
                "data": [],
                "layout": {
                    "font": {"color": "white"},
                    "paper_bgcolor": "rgba(0,0,0,0)",
                    "plot_bgcolor": "rgba(0,0,0,0)",
                },
            }

        if interval >= max_length:
            total_count = max_length - 1
        else:
            total_count = interval - 1

        values = []
        colors = []
        for param in params[1:]:
            ooc_param = (stored_data[param]["ooc"][total_count] * 100) + 1
            values.append(ooc_param)
            if ooc_param > 6:
                colors.append("#f45060")
            else:
                colors.append("#91dfd2")

        new_figure = {
            "data": [
                {
                    "labels": params[1:],
                    "values": values,
                    "type": "pie",
                    "marker": {"colors": colors, "line": dict(color="white", width=2)},
                    "hoverinfo": "label",
                    "textinfo": "label",
                }
            ],
            "layout": {
                "margin": dict(t=20, b=50),
                "uirevision": True,
                "font": {"color": "white"},
                "showlegend": False,
                "paper_bgcolor": "rgba(0,0,0,0)",
                "plot_bgcolor": "rgba(0,0,0,0)",
                "autosize": True,
            },
        }
        return new_figure
    

    @app.callback(
    Output('result_graph_id', 'figure'),
    [Input('analyze-submit-button', 'n_clicks')],
    [State('result_graph_id', 'figure')]
    )
    def update_graph(n_clicks, figure):
        if n_clicks == 0:
            return dash.no_update
        if n_clicks > 0:
        # Replace this with your own animation plot
            fig = plot_probabilities(data_)
            return fig
        

    @app.callback(
    Output('frame_data', 'srcDoc'),
    [Input('analyze-submit-button', 'n_clicks')],
    [State('frame_data', 'srcDoc')]
    )
    def update_frame(n_clicks, figure):
        j=50
        if n_clicks == 0:
            return dash.no_update
        if n_clicks > 0:
            while j<70:
                j+=1
            # Replae this with your own animation plot
                return plot_explanation(data_.iloc[j]).as_html()