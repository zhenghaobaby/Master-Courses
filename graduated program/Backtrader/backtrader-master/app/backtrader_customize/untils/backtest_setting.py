# Author : zhenghaobaby
# Time : 2020/1/25 16:36
# File : backtest_setting.py
# Ide : PyCharm

from backtrader_customize.Observer.OrderObserver import OrderObserver
import backtrader as bt
import pandas as pd

def backtest_setting(df, order_log, check_freq_check,tgt_freq,slip_pct,fix_size=1):

    check_freq = pd.Timedelta(pd.Series(df.index.values.tolist()).diff().mode()[0])
    unit_dict = {'D':'Days','min':'Minutes'}
    tgt_freq_unit = unit_dict[''.join([i for i in tgt_freq if i.isalpha()])]
    tgt_freq_n = int(''.join([i for i in tgt_freq if i.isnumeric()]))

    if check_freq % pd.Timedelta('1D') == pd.Timedelta(0):
        if check_freq.days >=1:
            check_freq_n = int(check_freq/pd.Timedelta('1D'))
            check_freq_unit = 'Days'
    else:
        check_freq_n = int(check_freq/pd.Timedelta('1min'))
        check_freq_unit = 'Minutes'

    ## First add the Original data - smaller timeframes
    cerebro = bt.Cerebro()

    if check_freq_check == tgt_freq:
        if tgt_freq!="1D":
            df = df.resample(tgt_freq,closed='right').agg({'close': 'last', 'open': 'first', 'high': 'max', 'low': 'min'})
            df.index = df.index.shift(1)
        else:
            df = df.resample(tgt_freq).agg(
                {'close': 'last', 'open': 'first', 'high': 'max', 'low': 'min'})

        df.dropna(inplace=True)

        data = bt.feeds.PandasData(dataname = df, volume=None,name='fx')
        cerebro.adddata(data)

    else:
        data = bt.feeds.PandasData(dataname = df,name = 'fx', volume=None,timeframe = check_freq_unit,compression = check_freq_n)
        cerebro.replaydata(data,
                           timeframe = getattr(bt.TimeFrame,tgt_freq_unit),
                           compression = tgt_freq_n,
                           rightedge=True)


    cerebro.broker = bt.brokers.BackBroker(slip_fixed = slip_pct, slip_open=True,slip_limit = True,slip_match = True,slip_out=False)
    cerebro.broker.setcash(100000000)

    cerebro.addobserver(OrderObserver,order_log=order_log)
    cerebro.addsizer(bt.sizers.FixedSize,stake = fix_size)
    return cerebro

