# Author : zhenghaobaby
# Time : 2020/1/12 12:38
# File : OrderObserver.py
# Ide : PyCharm


from __future__ import (absolute_import,division,print_function,unicode_literals)
import backtrader as bt
import pandas as pd

class OrderObserver(bt.observer.Observer):

    lines = ('ref','createdPrice','createdSize','executedPrice','executedValue','executedSize','OrderType',
             'Status','StopLoss','TargetValue','tradeid',
             'ref1','createdPrice1','createdSize1','executedPrice1','executedValue1','executedSize1','OrderType1',
             'Status1','StopLoss1','TargetValue1','tradeid1')

    plotinfo = dict(plot=False,subplot=False,plotlinelables=False)

    def __init__(self,order_log):
        self.order_log = order_log

    def next(self):
        results = []
        close =self.data.close[0]
        open = self.data.open[0]
        high = self.data.high[0]
        low = self.data.low[0]
        day = str(self.datas[0].datetime.date(0))
        time = str(self.datas[0].datetime.time(0))
        datetime = pd.to_datetime(day+" "+time)
        pos = self._owner.getposition().size
        for order in self._owner._orderspending:
            if order.status in [bt.Order.Completed]:
                results.append([
                    order.ref,
                    order.created.price,
                    order.created.size,
                    order.executed.price,
                    order.executed.value,
                    order.executed.size,
                    order.info,
                    order.status,
                    order.tradeid,
                ])

        if len(results)==0:  ##there is no order
            self.order_log['datetime'].append(datetime)
            self.order_log['open'].append(open)
            self.order_log['close'].append(close)
            self.order_log['high'].append(high)
            self.order_log['low'].append(low)
            self.order_log['ref'].append(0)
            self.order_log['createdPrice'].append(0)
            self.order_log['createdSize'].append(0)
            self.order_log['executedPrice'].append(0)
            self.order_log['executedValue'].append(0)
            self.order_log['executedSize'].append(0)
            self.order_log['OrderType'].append(0)
            self.order_log['Status'].append(0)
            self.order_log['StopLoss'].append(0)
            self.order_log['TargetValue'].append(0)
            self.order_log['tradeid'].append(-1)
            self.order_log['pos'].append(pos)

        if len(results)>0:  ##order are avaliable
            for items in results:
                self.order_log['datetime'].append(datetime)
                self.order_log['open'].append(open)
                self.order_log['close'].append(close)
                self.order_log['high'].append(high)
                self.order_log['low'].append(low)
                self.order_log['ref'].append(items[0])
                self.order_log['createdPrice'].append(items[1])
                self.order_log['createdSize'].append(items[2])
                self.order_log['executedPrice'].append(items[3])
                self.order_log['executedValue'].append(items[4])
                self.order_log['executedSize'].append(items[5])
                self.order_log['OrderType'].append(items[6]['name'])
                self.order_log['Status'].append(items[7])
                self.order_log['StopLoss'].append(items[6]['price_loss'])
                self.order_log['TargetValue'].append(items[6]['price_target'])
                self.order_log['tradeid'].append(items[8])
                self.order_log['pos'].append(pos)




