# Author : zhenghaobaby
# Time : 2020/1/25 17:06
# File : fetch_df.py
# Ide : PyCharm

import os
import pandas as pd




def fetch_df(start,end):
    df = []
    for filename in os.listdir("data"):
        data_item = pd.read_csv("data/"+filename,header=None,parse_dates=[[0,1]],
                                usecols=[0,1,2,3,4,5])
        data_item.columns = ['datetime', 'open', 'high', 'low', 'close']
        data_item['datetime'] = data_item['datetime'].apply(lambda x: pd.to_datetime(x))
        data_item.index = data_item['datetime']
        del data_item['datetime']
        df.append(data_item)

    df = pd.concat(df)

    df = df[(df.index > start) & (df.index < end)]
    df.dropna(inplace=True)

    return df




