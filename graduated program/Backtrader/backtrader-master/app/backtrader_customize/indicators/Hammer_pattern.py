# Author : zhenghaobaby
# Time : 2020/3/11 20:04
# File : Hammer_pattern.py
# Ide : PyCharm

import backtrader as bt
import numpy as np


class Hammer_pattern(bt.Indicator):

    lines = ('slope','Hammer')

    params = dict(
        period = 5,
        body_ratio = 0.3,
        shadow_ratio = 0.2,
    )

    def __init__(self):
        self.addminperiod(self.p.period)
        self.lag = self.p.period
        self.body_ratio = self.p.body_ratio
        self.shadow_ratio = self.p.shadow_ratio
        self.close_price = self.data.close

    def next(self):
        close = np.asarray(self.close_price.get(size=self.p.period))
        close = (close-close.mean())/close.std()

        x = np.arange(self.p.period)
        x = (x-x.mean())/x.std()
        poly = np.polyfit(x, close, 1)

        if self.data.high[0] == self.data.low[0]:
            self.l.slope[0] = self.l.slope[-1]
            self.l.Hammer[0] = False
        else:

            flag1 = (abs(self.data.close[0]-self.data.open[0])/(self.data.high[0]-self.data.low[0]))<self.body_ratio
            flag2 = ((self.data.high[0]-max(self.data.close[0],self.data.open[0]))/(self.data.high[0]-self.data.low[0]))<self.shadow_ratio

            self.l.slope[0] = poly[0]
            self.l.Hammer[0] = flag1 and flag2