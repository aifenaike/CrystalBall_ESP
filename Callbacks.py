import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.express as px
import pandas as pd
import numpy as np
import plots
import utils
import preprocessing 
import dash_tables
import os
import io
import base64



path = os.path.abspath(os.path.dirname(__file__))

def extract_stuffs(file_name):
    f = file_name.split('.')[0]
    f1 = f.split('_')[1]
    f1 = f1.split('0')[0]
    f4,f5 = f1.split('v')[0],f1.split('v')[1]
    lis_word = list((f4,f5))
    key = {'cclh':'Cupcake Light Hearted','t':'Truly','wc':'White Claw',
    'bls':'Bud Light Seltzer'}
    if lis_word[0].lower() in key.keys():
        lis_word[0] = key[lis_word[0].lower()]
    elif lis_word[0].lower() not in key.keys():
        lis_word[0] = "A"
    if lis_word[1].lower() in key.keys():
        lis_word[1] = key[lis_word[1].lower()]
    elif lis_word[1].lower() not in key.keys():
        lis_word[1] = "B"
    return lis_word


options=[
                    {'label': 'Composite', 'value': '0'},
                    {'label': 'Advertisement', 'value': '1'},
                    {'label': 'Billboards', 'value': '2'},
                    {'label': 'Social Media', 'value': '3'},
                    {'label': 'Product', 'value': '4'},
                    {'label': 'In Store Display', 'value': '5'},
                    {'label':'Section 6', 'value':6},
                    {'label':'Section 7','value':7},
                    {'label':'Section 8','value':8},
                    {'label':'Section 9','value':9},
                    {'label':'Section 10','value':10},
                    {'label':'Section 11','value':11},
                    {'label':'Section 12','value':12},
                    {'label':'Section 13','value':13},
                    {'label':'Section 14','value':14},
                    {'label':'Section 15','value':15}
                ]

all_options = {'Not Specified': ['Not Specified'],
            'Watch Other': ['Caucasian or White','Asian or Pacific Islander','Hispanic or Latino',
            'African American or Black'],
            'Watch Gender': ['Female','Male'],
            'Watch Age Range': ['18-24','25-29','30-34','35-39']}




"""
===============================================================================
Dash App Callbacks 
"""

def register_callbacks(app):

    @app.callback(
        Output('stored-diff', 'data'),
        Input('upload_difference_table', 'contents'),
        State('upload_difference_table', 'filename')
    )

    def save_to_path(diff, name):
        if diff is not None:
            
            content_type_diff, content_string_diff = diff.split(',')
        

            decoded_diff = base64.b64decode(content_string_diff)
            
            try:
                if 'xls' in name:
                    df = pd.read_excel(io.BytesIO(decoded_diff))
                
            except Exception as e:
                print(e)
                return html.Div([
                    'Only xlsx file is supported'
                ])

            return df.to_dict('records')


    @app.callback(
        Output('stored-emoji', 'data'),
        Input('upload_emoji_data', 'contents'),
        State('upload_emoji_data', 'filename')
    )

    def save_to_path(emoji, name):

        if emoji is not None:
            content_type_emoji, content_string_emoji = emoji.split(',')
        
            decoded_emoji = base64.b64decode(content_string_emoji)

            try:
                if 'xls' in name:
                    df = pd.read_excel(io.BytesIO(decoded_emoji))

            except Exception as e:
                print(e)
                return html.Div([
                    'Only xlsx file is supported'
                ])

            return df.to_dict('records')

    @app.callback(
        Output('stored-emotion', 'data'),
        Input('upload_emotion_data', 'contents'),
        State('upload_emotion_data', 'filename')
    )

    def save_to_path(emotion, name):

        if emotion is not None:
            content_type_emotion, content_string_emotion = emotion.split(',')
        
            decoded_emotion = base64.b64decode(content_string_emotion)

            try:
                if 'xls' in name:
                    df = pd.read_excel(io.BytesIO(decoded_emotion))

            except Exception as e:
                print(e)
                return html.Div([
                    'Only xlsx file is supported'
                ])

            return df.to_dict('records')

    @app.callback(
        [Output('sec_id', 'options'),
        Output('value_input','value'),
        Output('value_input','max')],
        [Input('stored-emotion', 'data')])
    def set_section_options(data):
        if data is not None:
            data2 = pd.DataFrame.from_records(data)
            data2 = data2[data2['Section ID'] !='Composite (wsecs & ssecs)']
            data2 = data2[data2['Section ID'] !='Composite (wsecs &ssecs)']
                
            n = data2['Section ID'].nunique()
            val = int(n/2)
            new = options[:val]
            max= val

            return new,val,max
        raise dash.exceptions.PreventUpdate
            
    @app.callback(
        [dash.dependencies.Output('level_id','options'),
        dash.dependencies.Output('level_id','value')],
        [dash.dependencies.Input('demo_id','value')]
    )
    def update_sidebar_dropdown(name):
        return [{'label':i, 'value': i} for i in all_options[name]], all_options[name][0]

    @app.callback(
        [dash.dependencies.Output('brand_id','options'),
        dash.dependencies.Output('brand_id','value')],
        dash.dependencies.Input('submit-button','n_clicks'),
        State('data_id','value'),
        State('upload_emotion_data', 'filename')
    )
    def update_content_dropdown(n,name,file_name):
        #if file_name is not None:
        if n != 0:
            if file_name is not None:
                brand = extract_stuffs(file_name)
                mini_options = {'Emoji_Data':brand,
                            'Emotion_Data': brand,
                            'Difference_Data': ['Both Brands']}
                return [{'label':i, 'value': i} for i in mini_options[name]], mini_options[name][0]
        raise dash.exceptions.PreventUpdate
        #else: 
            #return dash.no_update, dash.no_update


    @app.callback(
        Output('graph_id', 'figure'),
        #Output('inference_id', 'value'),
        Input('graphing_id', 'value'),
        Input('level_id', 'value'),
        Input('sec_id', 'value'),
        Input('demo_id', 'value'),
        Input('type_id','value'),
        State('stored-emoji', 'data'),
        State('stored-emotion', 'data'),
        State('upload_emotion_data', 'filename')
        )

    def update_graph(graphing_id_name,level_id_name, 
                    sec_id_name, demo_id_name, type_id_name,emoji,emotion,file_name):
                    if file_name is not None:
                        brand_name = extract_stuffs(file_name)
                        emoji = pd.DataFrame.from_records(emoji)
                        emotion = pd.DataFrame.from_records(emotion)

                        if sec_id_name == '0':
                            ssec = 'Standard Composite'
                            wsec = "What's-New Composite"
                        else:
                            ssec = '{}{}'.format('ssec',sec_id_name)
                            wsec = '{}{}'.format('wsec',sec_id_name)

                        if graphing_id_name == 2:
                            emotion_ext_1 = preprocessing.Extract_Emotion(emotion,ssec, demo_id_name, level_id_name)
                            emotion_ext_2 = preprocessing.Extract_Emotion(emotion,wsec, demo_id_name, level_id_name)
                            emotion = pd.concat([emotion_ext_1,emotion_ext_2])

                            if type_id_name == 1:
                                fig = plots.make_emotion_plot(emotion,ssec,wsec,'lineplot',brand_name)
                                return fig

                            elif type_id_name == 2:
                                fig = plots.make_emotion_plot(emotion,ssec,wsec,'Barchart',brand_name)
                                return fig


                        elif graphing_id_name == 1:
                            emoji_ext_1 = preprocessing.Extract_Emoji(emoji,ssec, demo_id_name, level_id_name)
                            emoji_ext_2 = preprocessing.Extract_Emoji(emoji,wsec, demo_id_name, level_id_name)
                            emoji = pd.concat([emoji_ext_1,emoji_ext_2])
                            
                            if type_id_name == 1:
                                fig = plots.make_emoji_plot(emoji,ssec,wsec,'lineplot',brand_name)
                                return fig

                            elif type_id_name == 2:
                                fig = plots.make_emoji_plot(emoji,ssec,wsec,'Barchart',brand_name)
                                return fig
                    else:
                        return dash.no_update

        
    

    @app.callback(
        [Output('Data', 'data'),
        Output('Data', 'columns'),
        Output('Data', 'style_data_conditional'),
        Output('legend_id', 'children')],
        [Input('brand_id', 'value'),
        Input('data_id', 'value')],
        [State('stored-diff', 'data'),
        State('stored-emoji', 'data'),
        State('stored-emotion', 'data'),
        State('upload_emotion_data', 'filename')]
    )
    def update_table(brand_id_name,data_id_name,difference_df,emoji_count, emotion_score, file_name):
        if file_name is not None:
            brand_name = extract_stuffs(file_name)
            difference_df = pd.DataFrame.from_records(difference_df)
            
            emoji_count = pd.DataFrame.from_records(emoji_count)
            emotion_score = pd.DataFrame.from_records(emotion_score)
            
            emoji,emotion = dash_tables.prepare(emoji_count,emotion_score,brand_name)
            if data_id_name == 'Emoji_Data':
                if brand_id_name == f'{brand_name[0]}':
                    cup,truly = dash_tables.extract_cup_truly(emoji,brand_name)
                    columns=[{"name": i, "id": i, "deletable": True} for i in cup.columns]
                    data=cup.to_dict("records")
                    return data,columns,dash.no_update,dash.no_update
                elif brand_id_name == f'{brand_name[1]}':
                    cup,truly = dash_tables.extract_cup_truly(emoji,brand_name)
                    columns=[{"name": i, "id": i, "deletable": True} for i in truly.columns]
                    data=truly.to_dict("records")
                    return data,columns,dash.no_update,dash.no_update
            elif data_id_name == 'Emotion_Data':
                if brand_id_name == f'{brand_name[0]}':
                    cup,truly = dash_tables.extract_cup_truly(emotion,brand_name)
                    columns=[{"name": i, "id": i, "deletable": True} for i in cup.columns]
                    data=cup.to_dict("records")
                    return data,columns,dash.no_update,dash.no_update
                elif brand_id_name == f'{brand_name[1]}':
                    cup,truly = dash_tables.extract_cup_truly(emotion,brand_name)
                    columns=[{"name": i, "id": i, "deletable": True} for i in truly.columns]
                    data=truly.to_dict("records")
                    return data,columns,dash.no_update,dash.no_update
            else:
                    df = dash_tables.extract_diff(difference_df)
                    (styles, legend) = utils.discrete_background_color_bins(df,columns=['Linear A-B'])
                    columns=[{"name": i, "id": i, "deletable": True} for i in df.columns]
                    data = df.to_dict("records")
                    return data,columns,styles,legend
        raise dash.exceptions.PreventUpdate

            