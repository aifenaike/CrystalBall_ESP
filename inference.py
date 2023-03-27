import pandas as pd
import numpy as np

def summary(df_1, df_2):

    # if df_1 or df_2 == None:
    #     raise ValueError("Dataframe cannot be empty")
    
    df_1['percent_count'] = df_1['count']/sum(df_1['count'])*100

    df_2['percent_count'] = df_2['count']/sum(df_2['count'])*100
    total_percentage_2 = sum(df_2['percent_count'])

    neg_1 = df_1[df_1['weight'] < 0]
    percent_neg_1 = round(neg_1['percent_count'].sum(), 2)


    pos_1 = df_1[~df_1['weight'].isin(neg_1['weight'])]
    percent_pos_1 = round(pos_1['percent_count'].sum(), 2)



    df_2['percent_count'] = df_2['count']/sum(df_2['count'])*100

    df_2['percent_count'] = df_2['count']/sum(df_2['count'])*100
    total_percentage_2 = sum(df_2['percent_count'])

    neg_2 = df_2[df_2['weight'] < 0]
    percent_neg_2 = round(neg_2['percent_count'].sum(), 2)

    pos_2 = df_2[~df_2['weight'].isin(neg_2['weight'])]
    percent_pos_2 = round(pos_2['percent_count'].sum(), 2)


    return [percent_neg_1, percent_pos_1, percent_neg_2, percent_pos_2] 



def interprete(first, second, third, fourth, sec):
    r_statement = " "
    if first > second:
        print(r_statement.join("The  negative reactions of {} ({}%) is greater than {} ({}%). Therefore, it is advised that {} improve their {}".format('A', first, 'B', second, 'A', sec)))

    elif first < second:
        print(r_statement.join("The negative reactions of {} ({}%) is greater than {} ({}%). Therefore, it is advised that {} improve their {}".format('B', second, 'A', first, 'B', sec)))
        if third > fourth:
            print(r_statement +".Also, " +  "The  positive reactions of {} ({}%) is greater than {} ({}%). \
                    Therefore, it is advised that {} keep at their {}".format('A', third, 'B', fourth, 'A', sec))
                    
        elif third < fourth:
            print(r_statement + ".Also, " + "The  positive reactions of {} ({}%) is greater than {} ({}%).\
                Therefore, it is advised that {} improve their {}".format('B', third, 'A', fourth, 'B', sec))

