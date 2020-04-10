# Author : zhenghaobaby
# Time : 2020/3/13 18:30
# File : pattern_recognize.py
# Ide : PyCharm


from backtrader_customize.influx.fetch_df import fetch_df
import matplotlib
import plotly
import numpy as np
import pandas as pd
from sklearn import linear_model

import plotly.graph_objects as go
from numpy.lib.stride_tricks import as_strided as stride
import pytz

def roll(df, w, **kwargs):
    v = df.values
    d0, d1 = v.shape
    s0, s1 = v.strides

    a = stride(v, (d0 - (w - 1), w, d1), (s0, s0, s1))

    rolled_df = pd.concat({
        row: pd.DataFrame(values, columns=df.columns)
        for row, values in zip(df.index, a)
    })

    return rolled_df.groupby(level=0, **kwargs)

def linear_slope(data):
    y = np.array(data.tolist())
    y = (y-np.mean(y))/np.std(y)
    x = np.arange(len(y))
    x = (x-np.mean(x))/np.std(x)

    poly = np.polyfit(x,y,1)
    return poly[0]


    # x = x.reshape((len(x),1))
    # reg = linear_model.LinearRegression(fit_intercept=False)
    # reg.fit(x,y)
    # k = reg.coef_
    # print("polyfit:%f, sklearn:%f"%(poly[0],k[0]))
    # return reg.coef_[0]

def hammer(row,body_ratio=0.3,shadow_ratio=0.2):
    open = row['open']
    high = row['high']
    low = row['low']
    close = row['close']

    flag_1 = abs(close-open)/(high-low)<body_ratio
    flag_2 = (high-max(close,open))/(high-low)<shadow_ratio

    return flag_1 and flag_2


def find_fractal(df):
    df_t = df.copy()
    df_t ['dir'] = np.sign(df_t['close'] - df_t['open'])
    df_t['fractal'] = 0
    u_c= pd.DataFrame([df_t['high'] < df_t['high'].shift(1), df_t['high'].shift(1) < df_t['high'].shift(2),\
              df_t['high'].shift(2) > df_t['high'].shift(3), df_t['high'].shift(3)>df_t['high'].shift(4)]).all()
    d_c= pd.DataFrame([df_t['low'] > df_t['low'].shift(1), df_t['low'].shift(1) > df_t['low'].shift(2),\
              df_t['low'].shift(2) < df_t['low'].shift(3), df_t['low'].shift(3)<df_t['low'].shift(4)]).all()
    df_t['fractal'][u_c] = -1
    df_t['fractal'][d_c] = 1
    return df_t['fractal']




def Shooting_star(row,body_ratio=0.3,shadow_ratio=0.2):
    open = row['open']
    high = row['high']
    low = row['low']
    close = row['close']

    flag_1 = abs(close - open) / (high - low) < body_ratio
    flag_2 = (min(close, open)-low) / (high - low) < shadow_ratio

    return flag_1 and flag_2


def Bullish_Engulfing(row):

    flag_1 = (row.iloc[0,:]['open']-row.iloc[0,:]['close'])>0
    flag_2 = (row.iloc[1,:]['open']-row.iloc[1,:]['close'])<0
    flag_3 = row.iloc[1,:]['close']>row.iloc[0,:]['open']
    flag_4 = row.iloc[1,:]['open']<row.iloc[0,:]['close']

    return flag_1 and flag_2 and flag_3 and flag_4


def Bearish_Engulfing(row):
    flag_1 = (row.iloc[0, :]['open'] - row.iloc[0, :]['close']) < 0
    flag_2 = (row.iloc[1, :]['open'] - row.iloc[1, :]['close']) > 0
    flag_3 = row.iloc[1, :]['close'] < row.iloc[0, :]['open']
    flag_4 = row.iloc[1, :]['open'] > row.iloc[0, :]['close']
    return flag_1 and flag_2 and flag_3 and flag_4



start = "2019-01-01"
end = "2020-01-01"
local_tz='Asia/Singapore'
data_tz='EST5EDT'


localtime = pytz.timezone(local_tz)
start = pd.to_datetime(start)
start = localtime.localize(start).tz_convert(data_tz)
start = start.strftime('%Y-%m-%d %H:%M:%S')
end = pd.to_datetime(end)
end = localtime.localize(end).tz_convert(data_tz)
end = end.strftime('%Y-%m-%d %H:%M:%S')

data = fetch_df(start=start,end=end)
data.index = pd.to_datetime(data.index).tz_localize(None)
data.index = data.index.tz_localize(data_tz)
data.index = data.index.tz_convert(local_tz)
data.index = data.index.tz_localize(None)

data = data.resample('1D').agg({'open':'first','close':'last','high':'max','low':'min'})
data.dropna(inplace=True)

## Pattern shape recongnize
data_fractal = find_fractal(data).to_frame()
data['Hammer_type'] = data.apply(lambda x:1 if hammer(x) else 0,axis=1)
data['Shooting_star_type'] = data.apply(lambda x:1 if Shooting_star(x) else 0,axis = 1)
data['Bullish_engulfing_type'] = roll(data,2).apply(lambda x:Bullish_Engulfing(x))
data['Bullish_engulfing_type'] = data['Bullish_engulfing_type'].shift(1)
data['Bearish_engulfing_type'] = roll(data,2).apply(lambda x:Bearish_Engulfing(x))
data['Bearish_engulfing_type'] = data['Bearish_engulfing_type'].shift(1)
## slope
data['slope'] = data['close'].rolling(5).apply(lambda x:linear_slope(x))


##  Pattern shape recongnize
data['Hammer'] = data.apply(lambda x: 1 if x['slope']<-0.5 and x['Hammer_type'] else 0,axis=1)
data['Shooting_star'] = data.apply(lambda x: 1 if x['slope']>0.5 and x['Shooting_star_type'] else 0, axis=1)
data['Bullish_engulfing'] = data.apply(lambda x: 1 if x['slope']<-0.5 and x['Bullish_engulfing_type'] else 0,axis=1)
data['Bearish_engulfing'] = data.apply(lambda x: 1 if x['slope']>0.5 and x['Bearish_engulfing_type'] else 0,axis=1)
data = pd.concat([data,data_fractal],axis=1)



## plot signal
Hammer_signal = data[data['Hammer']==1]
shooting_star_signal = data[data['Shooting_star']==1]
Bearish_engulfing_signal = data[data['Bearish_engulfing']==1]
Bullish_engulfing_signal = data[data['Bullish_engulfing']==1]
fractal_pos_signal = data[data['fractal']==1]
fractal_neg_signal = data[data['fractal']==-1]



fig = go.Figure(data=[go.Candlestick(
    x=data.index,
    open = data['open'],
    high = data['high'],
    low = data['low'],
    close = data['close'],
    name='OHLC'
)])



fig.add_trace(go.Scatter(
     x=Hammer_signal.index,
     y=Hammer_signal['close'],
     mode="markers",
     marker_color='blue',
     marker=dict(size=11, symbol='star-diamond-dot'),
     name='Hammer')
)

fig.add_trace(go.Scatter(
     x=shooting_star_signal.index,
     y=shooting_star_signal['close'],
     mode="markers",
     marker_color='deepskyblue',
     marker=dict(size=11, symbol='x'),
     name='Shooting star')
)

fig.add_trace(go.Scatter(
     x=Bullish_engulfing_signal.index,
     y=Bullish_engulfing_signal['close'],
     mode="markers",
     marker_color='yellow',
     marker=dict(size=11, symbol='triangle-up'),
     name='Bullish_engulfing')
)

fig.add_trace(go.Scatter(
     x=Bearish_engulfing_signal.index,
     y=Bearish_engulfing_signal['close'],
     mode="markers",
     marker_color='darkslategray',
     marker=dict(size=11, symbol='triangle-down'),
     name='Bearish_engulfing')
)



fig.add_trace(go.Scatter(
     x=fractal_pos_signal.index,
     y=fractal_pos_signal['close'],
     mode="markers",
     marker_color='brown',
     marker=dict(size=11, symbol='diamond'),
     name='fractal pos')
)

fig.add_trace(go.Scatter(
     x=fractal_neg_signal.index,
     y=fractal_neg_signal['close'],
     mode="markers",
     marker_color='black',
     marker=dict(size=11, symbol='square'),
     name='fractal neg')
)



fig.update_layout(
    title= {
        'text': 'EURUSD',
      'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'},
      font=dict(
        family="Courier New, monospace",
        size=20,
        color="#7f7f7f"
    )
    )

fig.show()

plotly.offline.plot(fig,"price_trades_plot.html", auto_open=False)