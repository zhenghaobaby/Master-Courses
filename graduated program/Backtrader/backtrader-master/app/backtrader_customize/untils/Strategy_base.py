# Author : zhenghaobaby
# Time : 2019/12/28 15:18
# File : Strategy_base.py
# Ide : PyCharm

from __future__ import (absolute_import,division,print_function,unicode_literals)
import backtrader as bt
import datetime
import pandas as pd

class Mystrategy(bt.Strategy):
    params = dict(
        underlying='USDJPY',
        start_time = '07:00',
        end_time = '23:45',
        force_time = '23:59',
        MTD = -0.2,
    )

    def __init__(self):
        self.fx_cash_transfer = {'SGD':1,"USD":1.13440,'JPY':0.0122,'CNY':0.1962,'CNH':0.1962,'CHF':1.3916,'CAD':1.0308}
        self.trade_id = 1
        self.orderlst=[]
        self.cur_len =1
        self.next_flag = 0
        self.MTD_STOP_LOSS = False
        self.enter_time = datetime.time(int(self.p.start_time[0:2]),int(self.p.start_time[3:5]))
        self.exit_time = datetime.time(int(self.p.end_time[0:2]),int(self.p.end_time[3:5]))
        self.force_close_time = datetime.time(int(self.p.force_time[0:2]),int(self.p.force_time[3:5]))
        self.MTD = self.broker.getvalue()
        self.buy_executed = {}
        self.sell_executed = {}
        self.ind_time = self.data.datetime()
        self.ind_close  = self.data.close
        self.bp = 0.01 if 'JPY' in self.p.underlying else 0.0001
        self.MTD_STOP_LOSS_LEVEL = (self.p.MTD if self.p.MTD!='inf' else -100000)/self.fx_cash_transfer[self.p.underlying[3:]]

    def log(self,txt,dt=None):
        dt = dt or self.datas[0].datetime.date(0)
        print("%s,%s"%(dt.isoformat(),txt))

    def notify_order(self, order):
        if self.MTD_STOP_LOSS:
            for ordum in self.orderlst:
                self.cancel(ordum)

        if order.status in [order.Accepted]:
            self.orderlst.append(order)


        if order.status in [order.Completed]:
            if order.info['name']==0 or order.info['name']==3:  ## only long/short order will use bracket order

                if order.info['name']==0: ## enter long
                    order.info['price_loss'] = self.data.open[0]-self.stop_level()
                    order.info['price_target'] = self.data.open[0]+self.tp_level()
                if order.info['name']==3: ## enter short
                    order.info['price_loss'] = self.data.open[0] + self.stop_level()
                    order.info['price_target'] = self.data.open[0] - self.tp_level()


                if order.isbuy():
                    if order.data._name in self.sell_executed.keys():
                        self.sell_executed.pop(order.data._name)

                    self.buy_executed[order.data._name] = len(self)

                    self.log(
                        'BUY EXECUTED,Price: %.6f, Cost: %.6f, Comm %.6f'%(
                            order.executed.price,
                            order.executed.value,
                            order.executed.comm
                        )
                    )

                    self.stop_long_loss = self.sell(tradeid=order.tradeid, exectype=bt.Order.Stop,
                                                    price=self.data.open[0] - self.stop_level())
                    self.stop_long_loss.addinfo(name=1, price_loss=self.data.open[0] - self.stop_level(),
                                                price_target=0)

                    self.stop_long_target = self.sell(tradeid=order.tradeid, exectype=bt.Order.Limit,
                                                      price=self.data.open[0] + self.tp_level(), oco=self.stop_long_loss)
                    self.stop_long_target.addinfo(name=2, price_target=self.data.open[0] + self.tp_level(),
                                                  price_loss=0)

                else:
                    if order.data._name in self.buy_executed.keys():
                        self.buy_executed.pop(order.data._name)

                    self.sell_executed[order.data._name] = len(self)


                    self.log('SELL EXECUTED, Price: %.6f, Cost: e%.6f, Comm %.6f'%(
                        order.executed.price,
                        order.executed.value,
                        order.executed.comm
                    ))

                    self.stop_short_loss = self.buy(tradeid=order.tradeid, exectype=bt.Order.Stop,
                                                    price=self.data.open[0] + self.stop_level())
                    self.stop_short_loss.addinfo(name=4, price_loss=self.data.open[0] + self.stop_level(),
                                                 price_target=0)

                    self.stop_short_target = self.buy(tradeid=order.tradeid, exectype=bt.Order.Limit,
                                                      price=self.data.open[0] - self.tp_level(),
                                                      oco=self.stop_short_loss)
                    self.stop_short_target.addinfo(name=5, price_loss=0, price_target = self.data.open[0]-self.tp_level())


        elif order.status in [order.Cancelled,order.Margin,order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return
        self.log('OPERATION PROFIT, GROSS %.6f, NET%.6F'%(trade.pnl, trade.pnlcomm))

    def buy_signal(self,pos):
        pass

    def sell_signal(self,pos):
        pass

    def close_signal(self,pos):
        pass

    def stop_level(self):
        if type(self.p.TP) == str:
            self.p.SL  = self.p.SL.lower()
            return float(self.p.SL.split('p')[0])/100*self.data.open[0]
        else:
            return self.p.SL*self.bp


    def tp_level(self):
        if type(self.p.TP) == str:
            self.p.TP = self.p.TP.lower()
            return float(self.p.TP.split('p')[0]) / 100 * self.data.open[0]
        else:
            return self.p.TP*self.bp

    def close_position(self):
        if self.position.size>0:
            for ordnum in self.orderlst:
                self.cancel(ordnum)
            self.orderlst = []
            self.close_long = self.close()
            self.close_long.addinfo(name=6,price_loss = 0, price_target=0)
            return

        if self.position.size<0:
            for ordnum in self.orderlst:
                self.cancel(ordnum)
            self.orderlst = []
            self.close_short = self.close()
            self.close_short.addinfo(name=7, price_loss=0, price_target=0)
            return
        else:
            return

    def execute_order(self):
        pos = self.position.size
        if self.buy_signal(pos):
            if self.position.size<0: ## we are in the short position
                for ordum in self.orderlst:
                    self.cancel(ordum)
                self.orderlst = []
                self.close_short = self.close()
                self.close_short.addinfo(name=7, price_loss=0, price_target=0)

            self.enter_long = self.buy(tradeid=self.trade_id)
            self.enter_long.addinfo(name = 0, price_loss = 0, price_target = 0)
            self.trade_id+=1

        ## need to go short
        elif self.sell_signal(pos):
            if self.position.size>0: ##we are in the long position
                for ordnum in self.orderlst:
                    self.cancel(ordnum)
                self.orderlst = []
                self.close_long = self.close()
                self.close_long.addinfo(name=6, price_loss=0, price_target=0)

            self.enter_short = self.sell(tradeid=self.trade_id)
            self.enter_short.addinfo(name=3,price_loss=0,price_target=0)
            self.trade_id+=1

        elif self.close_signal(pos):
            self.close_position()


    def next(self):
        bar_end_date = str(self.data.datetime.date(0))
        bar_end_time = str(self.data.datetime.time(0))
        bar_time = bar_end_date+" "+bar_end_time
        bar_time = pd.to_datetime(bar_time)


        """check whether is new month, or hit month stop loss point"""
        new_month = self.datetime.date(0).month - self.datetime.date(-1).month
        if new_month == 1:
            self.MTD_STOP_LOSS = False
            self.MTD = self.broker.getvalue()
        else:  ## the same month
            if self.broker.getvalue()-self.MTD<self.MTD_STOP_LOSS_LEVEL:  ## hit the loss level
                self.MTD_STOP_LOSS = True


        if not self.grid:  ## trading freq equal to check freq
            if not self.MTD_STOP_LOSS:
                if self.data.datetime.time()>=self.enter_time and self.data.datetime.time()<=self.exit_time:
                    self.execute_order()
                else:
                    if self.data.datetime().time()==self.force_close_time:
                        self.close_position()
            else:
                self.close_position()
                return
        else:
            if self.next_flag == 0:
                for i in range(len(self.grid)):
                    if self.grid[i] >= bar_time:
                        self.grid = self.grid[i:]
                        break
                self.next_flag = 1


            if not self.MTD_STOP_LOSS:
                """manage trading hour"""
                if self.data.datetime.time()>=self.enter_time and self.data.datetime.time()<=self.exit_time:
                    if not self.grid:  ## trading freq equal to check freq
                        self.execute_order()
                    else:  ## we are in the frequency
                        bar_end = (bar_time==self.grid[0])

                        if bar_end:
                            if len(self.grid)>1:
                                self.grid.pop(0)
                            self.execute_order()

                else:
                    if self.grid:
                        if bar_time == self.grid[0]:
                            self.grid.pop(0)

                    """force close position logic"""
                    if self.data.datetime.time(0)==self.force_close_time:
                        self.close_position()

            else:
                if self.grid:
                    if bar_time == self.grid[0]:
                        self.grid.pop(0)
                self.close_position()
                return


