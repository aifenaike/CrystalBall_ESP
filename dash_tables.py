import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import pandas as pd
import plots
import numpy as np
import preprocessing 
import emoji as em
import os


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

def extract_brand(df,brand_name,id='Section ID',id_a='ssec',id_b='wsec'):
    List=[]
    for i in df[id].values:
        if i.startswith(id_a[:3],0,3):
            List.append(f'{brand_name[0]}')
        elif i.startswith(id_b[:3],0,3):
            List.append(f'{brand_name[1]}')
        elif i == "What's-New Composite":
            List.append(f'{brand_name[1]}')
        else:
            List.append(f'{brand_name[0]}')
    return List

def extract_section(df,id='Section ID'):
    List=[]
    for i in df[id].values:
        if i in options.keys():
            List.append(options[i])
    return List

def Emoji_table(emoji):
    '''Returns a table of emoji, icon and occurences,
         emoji: the dataframe of emoji data,
         section_id: companies to be compared e.g wsec3,
         i : expected number of top emoji occurences'''
    list_emoji_found={'Fire':':fire:', 'HeartEyes':':heart_eyes:' ,'LyingFace':':lying_face:',
    'SmileyFace':':smiley:' ,'Sunglasses':':sunglasses:' ,'ThumbsDown':':thumbsdown:',
    'Vomit': ':nauseated_face:' ,'Yawn':':yawning_face:'}
    gcc = pd.Series(list_emoji_found)
    gccc= pd.DataFrame({'emoji':gcc.index, 'Emoticons':gcc.values})
    gccc['Emoticons'] = gccc['Emoticons'].apply(lambda x: em.emojize(x, use_aliases=True))
    emoji = emoji.merge(gccc,how='left',on='emoji')
    return emoji
def extract_cup_truly(df,brand_name):
    df_Cupcake= df[df['Brand']==f'{brand_name[0]}']
    df_Truly= df[df['Brand']==f'{brand_name[1]}']
    return df_Cupcake, df_Truly

def prepare(emoji_count,emotion_score,brand_name):
    required_emoji = ['emoji','Section ID','Demographic','Level','count']
    required_feelings = ['feeling','Section ID','Demographic','Level','emotionalScore']
    emoji = emoji_count[required_emoji]
    emotion = emotion_score[required_feelings]

    emoji = emoji[emoji['Section ID'] !='Composite (wsecs &ssecs)']
    emoji = emoji[emoji['Section ID'] !='Composite (wsecs & ssecs)']
    emotion = emotion[emotion['Section ID'] !='Composite (wsecs &ssecs)']
    emotion = emotion[emotion['Section ID'] !='Composite (wsecs & ssecs)']

    emoji['Brand'] = extract_brand(emoji,brand_name,id_a='ssec',id_b='wsec')
    emoji['Section ID'] = extract_section(emoji)
    emotion['Brand'] = extract_brand(emotion,brand_name,id_a='ssec',id_b='wsec')
    emotion['Section ID'] = extract_section(emotion)

    emoji = Emoji_table(emoji)
    return emoji,emotion

def extract_diff(difference_df):
    required_difference = ['Linear EB Score_A', 'Linear EB Score_B',  
        'Top Emoji by Clicks_A', 'Top Emoji by Clicks_B', 'Top Feelings_A',    
        'Top Feelings_B', 'Section ID_A', 'Section ID_B', 'Demographic',       
        'Level','Linear A-B']
    difference_df = difference_df[required_difference]
    difference_df = difference_df[difference_df['Section ID_A'] !='Composite (wsecs &ssecs)']
    difference_df = difference_df[difference_df['Section ID_A'] !='Composite (wsecs & ssecs)']
    difference_df = difference_df[difference_df['Section ID_B'] !='Composite (wsecs &ssecs)']
    difference_df = difference_df[difference_df['Section ID_B'] !='Composite (wsecs & ssecs)']
    difference_df['Section ID_A'] = extract_section(difference_df,id = 'Section ID_A')
    difference_df['Section ID_B'] = extract_section(difference_df, id ='Section ID_B' )
    #difference_df.drop(['Section ID_A'],1,inplace=True)
    difference_df['Linear A-B'] = difference_df['Linear A-B'].abs()
    #difference_df = difference_df.rename(columns={'Section ID_B':'Section ID'})
    return difference_df

