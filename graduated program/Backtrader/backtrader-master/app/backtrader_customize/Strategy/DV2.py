# Author : zhenghaobaby
# Time : 2020/2/1 16:36
# File : Bollinger_band.py
# Ide : PyCharm
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import backtrader as bt
from backtrader_customize.untils.Strategy_base import Mystrategy


class DV2(Mystrategy):
    params = dict(
        period = 252,
        maxpos = 20,
        minpos = -20,
        lowerbound = 30,
        upperbound = 70,
        TP=0,
        SL=0,
        indicator_name = [],
    )


    def __init__(self,grid):
        self.grid = grid
        super().__init__()
        self.dv2 = bt.indicators.DV2(self.data,period = self.p.period).dv2


    def buy_signal(self,pos):
        return self.dv2[-1]<self.p.lowerbound and self.dv2[0]>self.p.lowerbound and pos<self.p.maxpos

    def sell_signal(self,pos):
        return self.dv2[-1]>self.p.upperbound and self.dv2[0]<self.p.upperbound and pos>self.p.minpos


