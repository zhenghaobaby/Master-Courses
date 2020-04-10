# Author : zhenghaobaby
# Time : 2020/2/2 13:37
# File : data_transfer.py
# Ide : PyCharm

import  os
import pandas as pd


data_list = os.listdir("data")


for item in data_list:
    mm=2
    data_item = pd.read_csv("data/"+item,header=None,parse_dates=[[0,1]],usecols=[0,1,2,3,4,5])
    data_item.columns = ['datetime','open','high','low','close']
    data_item['datetime'] = data_item['datetime'].apply(lambda x:pd.to_datetime(x))
    data_item.index= data_item['datetime']
    del data_item['datetime']
    m=2







