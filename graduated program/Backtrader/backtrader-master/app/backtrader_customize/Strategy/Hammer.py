# Author : zhenghaobaby
# Time : 2020/3/11 20:13
# File : Hammer.py
# Ide : PyCharm

from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
import numpy as np
from backtrader_customize.untils.Strategy_base import Mystrategy
from backtrader_customize.indicators.Hammer_pattern import Hammer_pattern


class Hammer(Mystrategy):
    params = dict(
        period = 5,
        body_ratio = 0.3,
        shadow_ratio = 0.2,
        slope = 0.5,
        hold = 5,
        maxpos = 20,
        minpos = -20,
        TP=0,
        SL=0,
        indicator_name = [],
    )


    def __init__(self,grid):
        self.grid = grid
        super().__init__()
        self.ind = Hammer_pattern(self.data,period = self.p.period,body_ratio = self.p.body_ratio,
                                  shadow_ratio = self.p.shadow_ratio)
        self.close_price = self.data.close
        self.hammer  = self.ind.Hammer

    def buy_signal(self,pos):
        close = np.asarray(self.close_price.get(size=self.p.period))
        close = (close - close.mean()) / close.std()

        x = np.arange(self.p.period)
        x = (x - x.mean()) / x.std()
        poly = np.polyfit(x, close, 1)


        return poly[0]<-self.p.slope and self.hammer[0] and pos<self.p.maxpos

    def sell_signal(self,pos):
        return False

    def close_signal(self,pos):

        if self.buy_executed.get(self.datas[0]._name):
            if (len(self)-self.buy_executed.get(self.datas[0]._name))>=self.p.hold:
                return True
            else:
                return False
        return False

