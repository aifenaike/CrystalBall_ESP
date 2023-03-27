import numpy as np  
import pandas as pd
import os

path = os.path.abspath(os.path.dirname(__file__))



def Extract_Emoji(emoji_count,section_id, demographic, level):

    '''
    This function takes in section ID , demographic and level

    return: the extracted emoji count data from the specified difference characteristics in the emoji count data
    '''
    
    if demographic == 'Not Specified' and level == 'Not Specified':
        emoji = emoji_count[(emoji_count['Section ID']== section_id) & (emoji_count['Demographic'].isnull()) & (emoji_count['Level'].isnull())]
        
    elif demographic == 'Not Specified':
        emoji = emoji_count[(emoji_count['Section ID']== section_id) & (emoji_count['Demographic'].isnull()) & (emoji_count['Level']==level)]
    elif level == 'Not Specified':
        emoji = emoji_count[(emoji_count['Section ID']== section_id) & (emoji_count['Demographic']== demographic) & (emoji_count['Level'].isnull())]

    else:
        emoji = emoji_count[(emoji_count['Section ID']== section_id) & (emoji_count['Demographic']==demographic) & (emoji_count['Level']==level)]
    
    return emoji



def Extract_Emotion(emotion_score,section_id,demographic, level):


    '''
    This function takes in section ID , demographic and level

    return: the extracted emotion scores data from the specified difference characteristics in the emotion socres data


    '''

    if demographic == 'Not Specified' and level == 'Not Specified':
        emotion = emotion_score[(emotion_score['Section ID']== section_id) & (emotion_score['Demographic'].isnull()) & (emotion_score['Level'].isnull())]
        
    elif demographic == 'Not Specified':
        emotion = emotion_score[(emotion_score['Sect                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          ion ID']== section_id) & (emotion_score['Demographic'].isnull()) & (emotion_score['Level']==level)]
    elif level == 'Not Specified':
        emotion = emotion_score[(emotion_score['Section ID']== section_id) & (emotion_score['Demographic']== demographic) & (emotion_score['Level'].isnull())]

    else:
        emotion = emotion_score[(emotion_score['Section ID']== section_id) & (emotion_score['Demographic']==demographic) & (emotion_score['Level']==level)]
    
    return emotion


