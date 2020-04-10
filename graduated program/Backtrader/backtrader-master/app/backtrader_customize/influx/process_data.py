# Author : zhenghaobaby
# Time : 2020/1/25 16:59
# File : process_data.py
# Ide : PyCharm
from backtrader_customize.influx.fetch_df import fetch_df
import pandas as pd
import pytz


def process_data(start, end, local_tz='Asia/Singapore',data_tz='EST5EDT'):

    localtime = pytz.timezone(local_tz)
    start = pd.to_datetime(start)
    start = localtime.localize(start).tz_convert(data_tz)
    start = start.strftime("%Y-%m-%d %H:%M:%S")
    end = pd.to_datetime(end)
    end = localtime.localize(end).tz_convert(data_tz)
    end = end.strftime("%Y-%m-%d %H:%M:%S")

    df = fetch_df(start=start,end=end)
    df.index = pd.to_datetime(df.index).tz_localize(None)
    df.index = df.index.tz_localize(data_tz)
    df.index = df.index.tz_convert(local_tz)
    df.index = df.index.tz_localize(None)
    df.dropna(inplace=True)

    return df


