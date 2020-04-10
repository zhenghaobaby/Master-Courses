# Author : zhenghaobaby
# Time : 2020/1/12 16:18
# File : Trade_log_analysis.py
# Ide : PyCharm

import pandas as pd
import numpy as np
import os
from matplotlib.pyplot import savefig
import matplotlib.pyplot as plt


def Trade_Analysis(underlying,file_path,log_file,id):
    if 'JPY' in underlying:
        factor = 0.01
    else:
        factor = 1

    if not os._exists(file_path+"\\"+str(id)):
        os.makedirs(file_path+"\\"+str(id))

    del log_file['ref']
    del log_file['createdPrice']
    del log_file['createdSize']
    del log_file['executedValue']
    del log_file['Status']
    log_file.columns = ['datetime','open','close','high','low',
                        'executedPrice','executedSize','Order_type','SL','TP','id','pos']

    log_file.sort_values(by=['datetime','id'],inplace=True)
    log_file.loc[log_file['id']==0,'pos']=0
    log_file_for_trade = log_file[['datetime','open','close',
                                   'executedPrice','executedSize','Order_type','SL','TP','id','pos']]
    log_file_for_trade = log_file_for_trade[log_file_for_trade['id']!=-1]
    log_file_for_trade.index = np.arange(len(log_file_for_trade))

    """"deal with the trade log we want
        For every trade we use ['datetime','open','close',
        'executedPrice','executedSize','Order_type','SL','TP','id','pos'] """

    Trade_log = {
        'Open_time':[],
        'Close_time':[],
        'Order_type':[],
        'executed_size':[],
        'SL':[],
        'TP':[],
        'open_price':[],
        'close_price':[],
        'float_BP':[],
        'duration':[],
        'timereturn':[]
    }

    if len(log_file_for_trade)==0:
        return 0

    Order_stack = []
    Order_stack.append(log_file_for_trade.iloc[[0]])
    for i in range(1,len(log_file_for_trade)):
        order = log_file_for_trade.iloc[[i]]
        if order.iat[0,8]==0: ## close the position, we should close all the order in the stack
            for pre_order in Order_stack:
                Trade_log['Open_time'].append(pre_order.iat[0,0])
                Trade_log['Close_time'].append(order.iat[0,0])
                Trade_log['Order_type'].append(pre_order.iat[0,5])
                Trade_log['executed_size'].append(pre_order.iat[0,4])
                Trade_log['SL'].append(pre_order.iat[0,6])
                Trade_log['TP'].append(pre_order.iat[0,7])
                Trade_log['open_price'].append(pre_order.iat[0,3])
                Trade_log['close_price'].append(order.iat[0,3])
                Trade_log['float_BP'].append(order.iat[0,3]-pre_order.iat[0,3])
                Trade_log['duration'].append(pd.to_datetime(order.iat[0,0])-pd.to_datetime(pre_order.iat[0,0]))
                Trade_log['timereturn'].append(np.log(order.iat[0,3]/pre_order.iat[0,3]))
            Order_stack.clear()  ## end all the trade

        else:
            flag = 0
            for pre_order_index in range(len(Order_stack)):
                if order.iat[0,8]==Order_stack[pre_order_index].iat[0,8]: ## find a trade!!
                    flag=1
                    Trade_log['Open_time'].append(Order_stack[pre_order_index].iat[0,0])
                    Trade_log['Close_time'].append(order.iat[0, 0])
                    Trade_log['Order_type'].append(Order_stack[pre_order_index].iat[0,5])
                    Trade_log['executed_size'].append(Order_stack[pre_order_index].iat[0,4])
                    Trade_log['SL'].append(Order_stack[pre_order_index].iat[0,6])
                    Trade_log['TP'].append(Order_stack[pre_order_index].iat[0,7])
                    Trade_log['open_price'].append(Order_stack[pre_order_index].iat[0,0])
                    Trade_log['close_price'].append(order.iat[0, 3])
                    Trade_log['float_BP'].append(order.iat[0, 3] -Order_stack[pre_order_index].iat[0,3])
                    Trade_log['duration'].append(pd.to_datetime(order.iat[0, 0])- pd.to_datetime(Order_stack[pre_order_index].iat[0,0]))
                    Trade_log['timereturn'].append(np.log(order.iat[0, 3] / Order_stack[pre_order_index].iat[0,3]))
                    Order_stack.pop(pre_order_index)  ## this trade ends

                    break
            if flag==0:  ## means we create a new order
                Order_stack.append(order)

    Trade_log = pd.DataFrame(Trade_log)
    OrderType_list = {'0':'long', '1':'long SL', '2':'long TP', '3':'short',
                      '4':'short SL', '5':'short TP','6':'close long','7':'close short'}
    Trade_log['Order_type'].apply(lambda x:OrderType_list[str(x)])
    Trade_log['Profit'] = Trade_log['float_BP']*Trade_log['executed_size']
    Trade_log['float_BP'] = Trade_log['float_BP'].apply(lambda x:x*100*factor)

    """deal with summary analysis"""
    result_dict = {}
    result_dict['id'] = id
    result_dict['avg_duration'] = Trade_log['duration'].mean()
    result_dict['profit_factor'] = Trade_log[Trade_log['Profit']>0]['Profit'].sum()/abs(Trade_log[Trade_log['Profit']<0]['Profit'].sum())
    result_dict['max_win'] = Trade_log['Profit'].max()
    result_dict['max_loss'] = Trade_log['Profit'].min()
    result_dict['win_rate'] = len(Trade_log[Trade_log['Profit']>0])/len(Trade_log)
    result_dict['avg_win'] =  Trade_log[Trade_log['Profit']>0]['Profit'].mean()
    result_dict['avg_loss'] = Trade_log[Trade_log['Profit'] <0]['Profit'].mean()



    """Mark to Market"""
    log_file['cash'] = log_file['executedPrice']*-log_file['executedSize']
    log_file['cash'] = log_file['cash'].cumsum()
    log_file['close'] = log_file['close'].apply(lambda x:float(x))
    log_file['asset_value'] = log_file['close']*log_file['pos']
    log_file['YTD'] = log_file['cash']+log_file['asset_value']
    log_file['YTD'] = log_file['YTD']*factor
    log_file_for_pnl = log_file.drop_duplicates(subset=['datetime'],keep='last')
    log_file_for_pnl['bar_pnl'] = log_file_for_pnl['YTD'].diff().fillna(0)

    """Deal with MMD"""
    log_file_for_pnl['drawdown'] = log_file_for_pnl['YTD']-log_file_for_pnl['YTD'].cummax()
    result_dict['MMD'] = log_file_for_pnl['drawdown'].min()
    result_dict['Final pnl'] = log_file_for_pnl['YTD'].values[-1]

    """Resample for Daily pnl"""
    Daily_pnl = log_file_for_pnl[['datetime','open','close','pos','bar_pnl']]
    Daily_pnl.columns = ['datetime','open','close','pos','daily_pnl']
    Daily_pnl.index = Daily_pnl['datetime']
    del Daily_pnl['datetime']
    Daily_pnl = Daily_pnl.resample("D").agg({'open':'last','close':'last','pos':'last','daily_pnl':'sum'})
    Daily_pnl.dropna(subset=['open'],inplace=True)
    result_dict['sharpe_ratio'] = (Daily_pnl['daily_pnl'].mean()/Daily_pnl['daily_pnl'].std())*np.sqrt(252)
    result_dict['total_trades'] = len(Trade_log)


    result_dict = pd.DataFrame(result_dict,index= [0])

    """Resample fpr Monthly pnl"""
    Monthly_pnl = log_file_for_pnl[['datetime','open','close','pos','bar_pnl']]
    Monthly_pnl.columns = ['datetime','open','close','pos','MTD']
    Monthly_pnl.index = Monthly_pnl['datetime']
    del Monthly_pnl['datetime']
    Monthly_pnl = Monthly_pnl.resample("M").agg({'open': 'last', 'close': 'last', 'pos': 'last', 'MTD': 'sum'})
    result_dict['max_pos'] = log_file_for_pnl['pos'].max()
    result_dict['min_pos'] = log_file_for_pnl['pos'].min()


    """plot YTD,MTD,Daily pnl"""
    plt.figure(figsize=(30,16))
    plt.subplot(2,1,1)
    plt.plot(log_file_for_pnl['datetime'],log_file_for_pnl['YTD'].values,label='YTD')
    plt.plot(log_file_for_pnl['datetime'],log_file_for_pnl['drawdown'].values,label='Drawdown')
    plt.xlabel("datetime")
    plt.ylabel("pnl/amount")
    plt.legend()

    plt.subplot(2,1,2)
    Monthly_label = list(Monthly_pnl.index.values)
    for i in range(len(Monthly_label)):
        Monthly_label[i] = str(Monthly_label[i])
        Monthly_label[i] = Monthly_label[i][0:7]
    plt.bar(x=Monthly_label,height=Monthly_pnl['MTD'].values,label = 'pnl/amount')
    plt.xlabel('Month')
    plt.ylabel('cumpnl/amount')
    plt.xticks(rotation=90)
    plt.legend()

    savefig(file_path+f"\\{id}\\pnl.png")

    m = log_file_for_trade.loc[(log_file_for_trade['Order_type']=='long SL')|
                                  log_file_for_trade['Order_type']=='short SL']
    log_file_for_trade['Order_type'] = log_file_for_trade['Order_type'].apply(lambda x:OrderType_list[str(x)])
    Trade_log['Order_type'] = Trade_log['Order_type'].apply(lambda x:OrderType_list[str(x)])


    result_dict['SL_ratio'] = len(log_file_for_trade.loc[(log_file_for_trade['Order_type'] == 'long SL')|
                               (log_file_for_trade['Order_type'] == 'short SL')])/result_dict['total_trades']
    result_dict['TP_ratio'] = len(log_file_for_trade.loc[(log_file_for_trade['Order_type'] == 'long TP')|
                               (log_file_for_trade['Order_type'] == 'short TP')])/result_dict['total_trades']

    result_dict.to_csv(file_path+f"\\{id}\\Trade_analysis.csv",header=True,index=False)
    log_file_for_trade.to_csv(file_path+f"\\{id}\\Order_log.csv",header=True,index=False)
    Trade_log.to_csv(file_path+f"\\{id}\\trade_log.csv",header=True,index=False)
    print("Trade/Order Analysis is completed!!!")

    return True
