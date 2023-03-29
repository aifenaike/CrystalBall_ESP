
import dash_html_components as html
import dash_bootstrap_components as dbc
import colorlover

min_date = '2019-01-01'
max_date = '2020-01-01'
start_date = '2019-01-01'
end_date = '2019-01-01'

header = dbc.Jumbotron(
    [
        html.H1("ESP Analytics Dashboard", className="display-3"),
        html.P(
            " To elevate the accuracy of ESP fault recognition, \
                we leveraged probabilistic prediction instead of direct label classification.\
                In probabilistic prediction, we seek to predict the probability of a failure occurring rather than the exact status. \
                    This approach helped reduce the ratio of false-positive alarms.",
            className="lead",
        ),
        html.P("A comparison between two brands (A/B Testing). ", className=" font-italic"),
        html.Hr(className="my-2"),
        html.Div(id="blank_output", className="mb-4"),
    ],style={
                    'height':'auto',
                    'width':'auto',
                }
)


def discrete_background_color_bins(df, n_bins=5, columns='all'):
    
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))
