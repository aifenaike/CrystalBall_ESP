import numpy as np  
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go

path = os.path.abspath(os.path.dirname(__file__))


options={'Standard Composite':'Standard Composite',
             "What's-New Composite":"What's-New Composite",
            'ssec1':'Advertisement','wsec1': 'Advertisement',
            'ssec1':'Advertisement','wsec1': 'Advertisement',
            'ssec2':'Billboards','wsec2':'Billboards' ,
            'ssec3':'Social Media','wsec3':'Social Media',
             'ssec4':'Product','wsec4':'Product',
            'ssec5':'In Store Display','wsec5':'In Store Display',
            'ssec6':'Section 6','wsec6':'Section 6','ssec7':'Section 7','wsec7':'Section 7',
            'ssec8':'Section 8','wsec8':'Section 8','ssec9':'Section 9','wsec9':'Section 9',
            'ssec10':'Section 10','wsec10':'Section 10','ssec11':'Section 11','wsec11':'Section 11',
            'ssec12':'Section 12','wsec12':'Section 12','ssec13':'Section 13','wsec13':'Section 13',
            'ssec14':'Section 14','wsec14':'Section 14','ssec15':'Section 15','wsec15':'Section 15'}

def make_emotion_plot(emotion,section_id1,section_id2,chart_type,
                    brand_name=['Cupcake Light Hearted','Truly'],options=options):
    emotion_ssec = emotion[emotion['Section ID']==f'{section_id1}']
    emotion_ssec_sort = emotion_ssec.sort_values('emotionalScore',ascending='False')
    emotion_wsec = emotion[emotion['Section ID']==f'{section_id2}']
    emotion_wsec_sort = emotion_wsec.sort_values('emotionalScore',ascending='False')
    emotion_sort = pd.concat([emotion_wsec_sort,emotion_ssec_sort])
    
    List=[]
    for i in emotion_sort['Section ID'].values:
        if i.startswith('sse',0,3):
            List.append(f'{brand_name[0]}-{options[i]}')
        elif i.startswith('wse',0,3):
            List.append(f'{brand_name[1]}-{options[i]}')
        else:
            List.append(options[i])
    emotion_sort['Section ID'] = List

    if chart_type == 'lineplot':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
        x=emotion_wsec['feeling'],
        y=emotion_wsec['emotionalScore'],
        name=f'<b>{brand_name[1]}-{options[section_id2]}</b>',connectgaps=False
        ))

        fig.add_trace(go.Scatter(
        x=emotion_ssec['feeling'],
        y=emotion_ssec['emotionalScore'],
        name = f'<b>{brand_name[0]}-{options[section_id1]}</b>', # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
        ))
        fig.update_traces(textposition='bottom center')

        fig.update_layout(plot_bgcolor='#FFF',title_text=f'Feelings Score Contrast for {brand_name[0]} and {brand_name[1]}')

        return fig
    else:
        fig2 = go.Figure(data=[
            go.Bar(name=f'<b>{brand_name[1]}-{options[section_id2]}</b>', x=emotion_wsec['feeling'],
        y=emotion_wsec['emotionalScore']),
               go.Bar(name=f'<b>{brand_name[0]}-{options[section_id1]}</b>', x=emotion_ssec['feeling'],
        y=emotion_ssec['emotionalScore'])
               ])
        
        # bar chart
        #fig2 = px.bar(emotion_sort, x='feeling', y='emotionalScore',
                    #color='Section ID',barmode='group',title=f'Feelings Score Contrast for {brand_name[0]} and {brand_name[1]}',
                        #labels={'emotionalScore':'Feelings Score','feeling':'Emotion'})

        fig2.update_layout(plot_bgcolor='#FFF',barmode='group',xaxis=go.layout.XAxis(tickangle=45),
        title_text=f'Feelings Score Contrast for {brand_name[0]} and {brand_name[1]}')
        
        return fig2
        
def make_emoji_plot(emoji,section_id1,section_id2,chart_type,
                brand_name=['Cupcake Light Hearted','Truly'],options = options):
    emoji_ssec = emoji[emoji['Section ID']==f'{section_id1}']
    emoji_ssec_sort = emoji_ssec.sort_values('count',ascending='False')
    emoji_wsec = emoji[emoji['Section ID']==f'{section_id2}']
    emoji_wsec_sort = emoji_wsec.sort_values('count',ascending='False')
    emoji_sort = pd.concat([emoji_wsec_sort,emoji_ssec_sort])

    List=[]
    for i in emoji_sort['Section ID'].values:
        if i.startswith('sse',0,3):
            List.append(f'{brand_name[0]}-{options[i]}')
        elif i.startswith('wse',0,3):
            List.append(f'{brand_name[1]}-{options[i]}')
        else:
            List.append(options[i])
    emoji_sort['Section ID'] = List

    if chart_type == 'lineplot':
        fig = go.Figure()
        fig.add_trace(go.Scatter(
        x=emoji_wsec['emoji'],
        y=emoji_wsec['count'],
        name=f'<b>{brand_name[1]}-{options[section_id2]}</b>',connectgaps=False
        ))

        fig.add_trace(go.Scatter(
        x=emoji_ssec['emoji'],
        y=emoji_ssec['count'],
        name = f'<b>{brand_name[0]}-{options[section_id1]}</b>', # Style name/legend entry with html tags
        connectgaps=True # override default to connect the gaps
        ))
        fig.update_traces(textposition='bottom center')

        fig.update_layout(plot_bgcolor='#FFF',
        title_text=f'Emoji Activity Contrast for {brand_name[0]} and {brand_name[1]}')

        return fig
    else:
        ##bar chart
        fig2 = go.Figure(data=[
            go.Bar(name=f'<b>{brand_name[1]}-{options[section_id2]}</b>', x=emoji_wsec['emoji'],
        y=emoji_wsec['count']),
               go.Bar(name=f'<b>{brand_name[0]}-{options[section_id1]}</b>', x=emoji_ssec['emoji'],
        y=emoji_ssec['count'])
               ])
            
        
        #fig2 = px.bar(emoji_sort, x='emoji', y='count',
                    #color='Section ID',barmode='group',title=f'Emoji Activity Contrast for {brand_name[0]} and {brand_name[1]}',
                     #labels={'count':'Emoji Activity Count','emoji':'Emoji'})
        
        fig2.update_layout(plot_bgcolor='#FFF',barmode='group',xaxis=go.layout.XAxis(tickangle=45),
        title_text=f'Emoji Activity Contrast for {brand_name[0]} and {brand_name[1]}')
        
        return fig2
        
        
